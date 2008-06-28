"""
Functions to make working with databases easier. I{Currently only PostgreSQL}
"""

import re

# Loading ourselves before third party is bad, but we need to be able
# to raise our own exception if things go wrong
from chula import error, data

try:
    import psycopg2
    from psycopg2 import extensions, extras
except:
    raise error.MissingDependencyError('Psycopg2')


# Expose the psycopg2 exceptions
DataError = psycopg2.DataError
Databaserror = psycopg2.DatabaseError
Error = psycopg2.Error
IntegrityError = psycopg2.IntegrityError
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
            raise error.MalformedConnectionStringError

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
        Perform database commit
        """
        
        self.conn.commit()
        
    def rollback(self):
        """
        Perform query rollback
        """
        
        self.conn.rollback()
    
    def cursor(self, type='dict'):
        """
        Create database cursor

        @param type: Type of cursor to return
        @type type: string, I{dict} or I{tuple}
        @return: Instance
        """

        if type == 'tuple':
            return self.conn.cursor(cursor_factory=psycopg2.extensions.cursor)

        elif type == 'dict':
            return self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        else:
            msg = 'Invalid cursor type, use either tuple or dict'
            raise error.UnsupportedUsageError(append=msg)
    
#class SafetyCursor(psycopg2.extensions.cursor):
#    def execute(self, sql, args=None):
#        """
#        Simple factory to check that an update or delete statement aren't
#        being ran without a where clause.
#        """
#
#        sql = _checkForDanger(sql)
#
#        return super(SafetyCursor, self).execute(sql, args)
#
#class SafetyDictCursor(psycopg2.extras.DictCursor):
#    def execute(self, sql, args=None):
#        """
#        Simple factory to check that an update or delete statement aren't
#        being ran without a where clause.
#        """
#
#        sql = _checkForDanger(sql)
#        return super(SafetyDictCursor, self).execute(sql, args)
# 
#def _checkForDanger(sql):
#    """
#    Check that the passed sql statement has a where clause if it contains
#    either an update or delete statement.
#    """
#
#    danger = sql.upper()
#    if danger.find('UPDATE') >= 0 or danger.find('DELETE') >= 0:
#        if danger.find('WHERE') < 0:
#            msg = 'Please add a valid WHERE clause (use 1=1 to force)'
#            raise error.ExtremeDangerError(append=msg)
#
#    return sql

def cbool(input_):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it
    will return 'NULL' so as to insert a NULL value into the database.

    @param input_: String to be cleaned
    @type input_: String
    @return: String I{TRUE/FALSE}, or 'NULL'
    
    >>> print 'SET active = %s;' % cbool(True)
    SET active = TRUE;
    """
    
    if input_ in [None, '']:
        return 'NULL'
    
    input_ = str(input_).lower()
    if input_ in data.TRUE:
        return 'TRUE'

    elif input_ in data.FALSE:
        return 'FALSE'

    else:
        raise error.TypeConversionError(input_, 'sql boolean')

def cdate(input_, doquote=True, isfunction=False):
    """
    Returns a formatted string safe for use in SQL. If None or an empty
    string is passed, it will return 'NULL' so as to insert a NULL value
    into the database.
    
    B{Todo:}
    I{This function needs to be able to receive datetime.datetime types too.}
    
    @param input_: Date to be cleaned
    @type input_: String
    @return: String, or 'NULL'
    
    >>> print 'SET updated = %s;' % cdate('1/1/2005')
    SET updated = '1/1/2005';
    
    >>> print 'SET updated = %s;' % cdate('now()', isfunction=True)
    SET updated = now();
    """
    
    if input_ in [None, '']:
        return 'NULL'

    elif isfunction:
        return input_

    else:
        input_ = str(input_)
        if data.isdate(input_):
            if doquote:
                input_ = data.wrap(input_, "'")
        else:
            raise error.TypeConversionError(input_, 'sql date')

    return input_

def cfloat(input_):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it
    will return 'NULL' so as to insert a NULL value into the database.
    
    @param input_: Float to be cleaned
    @type input_: Anything
    @return: Float, or 'NULL'
    
    >>> print 'WHERE field = %s;' % cfloat("45")
    WHERE field = 45.0;
    """
    
    # Check if the data passed is a NULL value
    if input_ is None or str(input_).lower() == 'null' or input_ == '':
        return 'NULL'

    elif isinstance(input_, float):
        return input_

    try:
        return float(input_)
    except:
        raise error.TypeConversionError(input_, 'sql float')

def cint(input_):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it
    will return 'NULL' so as to insert a NULL value into the database.
    
    @param input_: Integer to be cleaned
    @type input_: Anything
    @return: Integer, or 'NULL'
    
    >>> print 'WHERE field = %s;' % cint("45")
    WHERE field = 45;
    """
    
    # Check if the data passed is a NULL value
    if input_ is None or str(input_).lower() == 'null' or input_ == '':
        return 'NULL'

    elif isinstance(input_, int):
        return input_

    try:
        return int(input_)
    except:
        raise error.TypeConversionError(input_, 'sql float')

def cregex(input_, doquote=True):
    """
    Returns a regular expression safe for use in SQL.  If None is
    passed if will raise an exception as None is not a valid regular
    expression.  The intented use is with regex based SQL expressions.


    @param input_: Value to evaluate
    @type input_: str
    @param doquote: I{OPTIONAL}: Wrapped in single quotes, defaults to B{True}
    @type doquote: bool
    @return: str
    """

    if data.isregex(input_):
        if doquote:
            return data.wrap(input_, "'")
        else:
            return input_
    else:
        raise error.TypeConversionError(input_, 'sql regex')

def cstr(input_, doquote=True, doescape=True):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it
    will return 'NULL' so as to insert a NULL value into the database.
    Single quotes will be escaped.
    
    @param input_: String to be cleaned
    @type input_: String
    @param doquote: I{OPTIONAL}: Wrapped in single quotes, defaults to B{True}
    @type doquote: bool
    @param doescape: I{OPTIONAL}: Escape single quotes, defaults to B{True}
    @type doescape: bool
    @return: String, or 'NULL'
    
    >>> print 'SET description = %s;' % cstr("I don't")
    SET description = 'I don''t';
    >>> print 'SET now = %s;' % cstr("CURRENT_TIME", doquote=False)
    SET now = CURRENT_TIME;
    """
    
    if input_ is None:
        return 'NULL'
    
    input_ = str(input_) 
    if doescape:
        escape = {"'":"''", "\\":"\\\\"}
        input_ = data.replace_all(escape, input_)

    if doquote:
        return data.wrap(input_, "'")
    else:
        return input_

def ctags(input_):
    """
    Returns a string safe for use in a sql statement

    @param: input_
    @type input_: Anything
    @return: 'NULL', or input_ string
    
    >>> print ctags('')
    NULL
    >>> print ctags('linux git foo')
    'foo git linux'
    """

    if input_ in [None, '']:
        return 'NULL'
    
    if isinstance(input_, list):
        input_ = ' '.join(input_)

    tags = data.tags2str(data.str2tags(input_))
    return "'%s'" % tags.lower()

def empty2null(input_):
    """
    Returns NULL if an empty string or None is passed, else returns the
    input_ string.

    @param: input_
    @type input_: Anything
    @return: 'NULL', or input_ string
    
    >>> print empty2null('')
    NULL
    """

    if input_ in [None, '']:
        return 'NULL'
    else:
        return input_

def unquote(input_):
    """
    Return string not padded with single quotes.  This is useful to
    clean something changed by cstr()

    @param: input_
    @type input_: str
    @return: str, or input unchanged
    """

    if isinstance(input_, str):
        if input_.startswith("'") and input_.endswith("'"):
            input_ = input_[1:-1]

    return input_
