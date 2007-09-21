"""
Functions to make working with databases easier. I{Currently only PostgreSQL}
"""

import re
from chula import chulaException, data   
try:
    import psycopg2
    from psycopg2 import extensions, extras
except:
    raise chulaException.MissingDependancyError('psycopg2')

# Expose the psycopg2 exceptions
IntegrityError = psycopg2.IntegrityError
Databaserror = psycopg2.DatabaseError
DataError = psycopg2.DataError
Error = psycopg2.Error
InterfaceError = psycopg2.InterfaceError
InternalError = psycopg2.InternalError
NotSupportedError = psycopg2.NotSupportedError
OperationalError = psycopg2.OperationalError
ProgrammingError = psycopg2.ProgrammingError

class Datastore(object):
    """
    The Database class creates an instance of Postgresql. Currently this is
    only implemented using psycopg2.
    """
    
    def __init__(self, conn, passwd=''):
        """
        Datastore constructor. Creates an instance of the Datastore class.
        
        The connection string is a tuple with the following values in order:
            1. Database type B{(Currently the only supported option is: pg)}
            2. Username
            3. Host
            4. Database name
            
            eg: pg:username@server/databasename
        
        @param conn: Connection string
        @type conn: String
        @param passwd: Database password
        @type passwd: String
        @return: Instance
        
        >>> conn = Datastore('pg:chula@localhost/chula_test', 'passwd')
        >>> cursor = conn.cursor()
        >>> cursor.execute('SELECT * FROM cars LIMIT 1;')
        >>> data = cursor.fetchone()
        >>> print data
        [1, 'Honda', 'Civic']
        >>> print data['make']
        Honda
        >>> print dict(data)
        {'model': 'Civic', 'make': 'Honda', 'uid': 1}
        >>>
        >>> cursor = conn.cursor(type='tuple')
        >>> cursor.execute('SELECT * FROM cars LIMIT 1;')
        >>> print cursor.fetchone()
        (1, 'Honda', 'Civic')
        >>>
        >>> conn.close()
        """
        
        m = re.match(r'^(?P<type>pg):'
                     r'(?P<user>[-a-zA-Z0-9]+)@'
                     r'(?P<host>[-a-zA-Z0-9]+)/'
                     r'(?P<db>[-a-zA-Z0-9_]+)$', conn)

        if m is None:
            raise chulaException.MalformedConnectionStringError

        parts = m.groupdict()
        parts['pass'] = passwd

        conn = 'host=%(host)s dbname=%(db)s user=%(user)s password=%(pass)s'
        self.conn = psycopg2.connect(conn % parts)
        
    def set_isolation(self, level=1):
        """
        Toggle the isolation level. Here are the available
        isolation levels:
            - 0 = No isolation
            - 1 = READ COMMITTED (the default)
            - 3 = SERIALIZABLE
        
        @param level: Isolation level
        @type level: Integer
        """
        
        self.conn.set_isolation_level(level)
    
    def close(self):
        """
        Destroy a database connection object
        """
        
        self.conn.close()
        
    def commit(self):
        """
        Perform database commit.
        """
        
        self.conn.commit()
        
    def rollback(self):
        """
        Perform query rollback.
        """
        
        self.conn.rollback()
    
    def cursor(self, type='dict'):
        """
        Create database cursor.
        
        @param type: Type of cursor to return
        @type type: string, I{dict} or I{tuple}
        @return: Instance
        """

        if type == 'tuple':
            return self.conn.cursor(cursor_factory=SafetyCursor)

        elif type == 'dict':
            return self.conn.cursor(cursor_factory=SafetyDictCursor)

        else:
            msg = 'Invalid cursor type, use either tuple or dict'
            raise chulaException.UnsupportedUsageError(append=msg)
    
class SafetyCursor(psycopg2.extensions.cursor):
    def execute(self, sql, args=None):
        """
        Simple factory to check that an update or delete statement aren't
        being ran without a where clause.
        """
        sql = _checkForDanger(sql)
        return super(SafetyCursor, self).execute(sql, args)

class SafetyDictCursor(psycopg2.extras.DictCursor):
    def execute(self, sql, args=None):
        """
        Simple factory to check that an update or delete statement aren't
        being ran without a where clause.
        """
        sql = _checkForDanger(sql)
        return super(SafetyDictCursor, self).execute(sql, args)
 
def _checkForDanger(sql):
    """
    Check that the passed sql statement has a where clause if it contains
    either an update or delete statement.
    """

    danger = sql.upper()
    if danger.find('UPDATE') >= 0 or danger.find('DELETE') >= 0:
        if danger.find('WHERE') < 0:
            msg = 'Please add a valid WHERE clause (use 1=1 to force)'
            raise chulaException.ExtremeDangerError(append=msg)

    return sql

def cbool(input):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it
    will return 'NULL' so as to insert a NULL value into the database.
    
    @param input: String to be cleaned
    @type input: String
    @return: String I{TRUE/FALSE}, or 'NULL'
    
    >>> print 'SET active = %s;' % cbool(True)
    SET active = TRUE;
    """
    
    if input in [None, '']:
        return 'NULL'
    
    input = str(input).lower()
    if input in data.TRUE:
        return 'TRUE'

    elif input in data.FALSE:
        return 'FALSE'

    else:
        raise chulaException.TypeConversionError(input, 'sql boolean')

def cdate(input, doquote=True, isfunction=False):
    """
    Returns a formatted string safe for use in SQL. If None or an empty
    string is passed, it will return 'NULL' so as to insert a NULL value
    into the database.
    
    B{Todo:}
    I{This function needs to be able to receive datetime.datetime types too.}
    
    @param input: Date to be cleaned
    @type input: String
    @return: String, or 'NULL'
    
    >>> print 'SET updated = %s;' % cdate('1/1/2005')
    SET updated = '1/1/2005';
    
    >>> print 'SET updated = %s;' % cdate('now()', isfunction=True)
    SET updated = now();
    """
    
    if input in [None, '']:
        return 'NULL'

    elif isfunction is True:
        return input

    else:
        if data.isdate(input) is True:
            if doquote is True:
                input = data.wrap(input, "'")
        else:
            raise chulaException.TypeConversionError(input, 'sql date')

    return input

def cfloat(input):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it
    will return 'NULL' so as to insert a NULL value into the database.
    
    @param input: Float to be cleaned
    @type input: Anything
    @return: Float, or 'NULL'
    
    >>> print 'WHERE field = %s;' % cfloat("45")
    WHERE field = 45.0;
    """
    
    # Check if the data passed is a NULL value
    if input is None or str(input).lower() == 'null' or input == '':
        return 'NULL'

    elif isinstance(input, float) is True:
        return input

    try:
        return float(input)
    except:
        raise chulaException.TypeConversionError(input, 'sql float')

def cint(input):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it
    will return 'NULL' so as to insert a NULL value into the database.
    
    @param input: Integer to be cleaned
    @type input: Anything
    @return: Integer, or 'NULL'
    
    >>> print 'WHERE field = %s;' % cint("45")
    WHERE field = 45;
    """
    
    # Check if the data passed is a NULL value
    if input is None or str(input).lower() == 'null' or input == '':
        return 'NULL'

    elif isinstance(input, int) is True:
        return input

    try:
        return int(input)
    except:
        raise chulaException.TypeConversionError(input, 'sql float')

def cstr(input, doquote=True, doescape=True):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it
    will return 'NULL' so as to insert a NULL value into the database.
    Single quotes will be escaped.
    
    @param input: String to be cleaned
    @type input: String
    @param doquote: I{OPTIONAL}: Wrapped in single quotes, defaults to B{True}
    @type doquote: Boolean
    @param doescape: I{OPTIONAL}: Escape single quotes, defaults to B{True}
    @type doescape: Boolean
    @return: String, or 'NULL'
    
    >>> print 'SET description = %s;' % cstr("I don't")
    SET description = 'I don''t';
    >>> print 'SET now = %s;' % cstr("CURRENT_TIME", doquote=False)
    SET now = CURRENT_TIME;
    """
    
    if input is None:
        return 'NULL'
    
    input = str(input) 
    if doescape:
        escape = {"'":"''", "\\":"\\\\"}
        input = data.replace_all(escape, input)

    if doquote:
        return data.wrap(input, "'")
    else:
        return input

def ctags(input):
    """
    Returns a string safe for use in a sql statement
    @param: input
    @type input: Anything
    @return: 'NULL', or input string
    
    >>> print ctags('')
    NULL
    >>> print ctags('linux git foo')
    'foo git linux'
    """

    if input in [None, '']:
        return 'NULL'
    
    if isinstance(input, list) is True:
        input = ' '.join(input)

    tags = data.tags2str(data.str2tags(input))
    return "'%s'" % tags.lower()

def empty2null(input):
    """
    Returns NULL if an empty string or None is passed, else returns the
    input string.
    @param: input
    @type input: Anything
    @return: 'NULL', or input string
    
    >>> print empty2null('')
    NULL
    """

    if input in [None, '']:
        return 'NULL'
    else:
        return input

