"""
Functions to make working with databases easier. I{Currently only PostgreSQL}
"""

from chula import data   
try:
    import psycopg2
    import psycopg2.extensions
    import psycopg2.extras
except:
    class psycopg2:
        class extensions:
            class cursor:
                def fetchall(self): pass
                def fetchmany(self): pass

# Expose the psycopg2 exceptions
IntegrityError = psycopg2.IntegrityError
DatabaseError = psycopg2.DatabaseError
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
            
        """
        
        # TODO: Add regex check on the connection string
        dbinfo = (conn[conn.find('@')+1:conn.find('/')],
                  conn[conn.find('/')+1:],
                  conn[conn.find(':')+1:conn.find('@')],
                  passwd)
        
        self.conn = psycopg2.connect(
            ('host=%s dbname=%s user=%s password=%s') % (dbinfo)
        )
        
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
            return self.conn.cursor(cursor_factory=Cursor)
        else:
            return self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    def execute(self, sql):
        """
        Execute I{sql} statement.
        
        @param sql: sql statement to execute
        @type sql: String
        @return: Cursor
        
            >>> conn = Datastore('pg:chula@localhost/chula_test', 'password')
            >>> rs = conn.cursor()
            >>> rs.execute("SELECT * FROM cars;")
            >>> sql = "INSERT INTO cars(make, model) VALUES('Honda', 'Civic');"
            >>> rs.execute(sql)
            >>> conn.commit()
            
        """
        
        #TODO: I think this function needs to be depricated?
        temp = sql.upper()
        print temp.find('DELETE')
        if temp.find('UPDATE') >= 0 or temp.find('DELETE') >= 0:
            if temp.find('WHERE') <= 0:
                raise Exception, 'Dummy, please try adding a WHERE clause!'
            
        return self.cursor().execute(sql)

class Cursor(psycopg2.extensions.cursor):
    """
    Custom cursor class to customize things a bit.
    """
    def fetchone(self):
        """
        Fetches the first record in a recordset.  It returns an object
        that is a pseudo dictionary, meaning you can loop thru it just
        as you would a normal python dictionary, but it's immutable and
        doesn't support all of the CPython dictionary methods.  Typically
        you will convert to a CPython dictionary in the event you would
        need this functionality using the dict() python function.
        
        B{Note:} If the recordset doesn't contain any data, fetchone() will
        return I{None}, not an empty dictionary.
        
        @return: Psuedo dictionary
        """
        return psycopg2._psycopg.cursor.fetchone(self)
        
    def fetchall(self):
        d = psycopg2.extensions.cursor.fetchall(self)
        return d
    
    def fetchmany(self):
        d = psycopg2.extensions.cursor.fetchmany(self)
        return d
    
def cbool(input):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it will
    return 'NULL' so as to insert a NULL value into the database.
    
    @param input: String to be cleaned
    @type input: String
    @return: String I{TRUE/FALSE}, or 'NULL'
    
        >>> print 'SET active = %s;' % cbool(True)
        SET active = TRUE;
    
    """
    
    if input is None or input == '': return 'NULL'
    
    if isinstance(input, str):
        true = [1, 'on', 't', 'true', 'y', 'yes', '1']
        false = [0, 'off', 'f', 'false', 'n', 'no', '0']
        input = input.lower()
    else:
        true = [True]
        false = [False]
        
    if input in true:
        return 'TRUE'
    elif input in false:
        return 'FALSE'
    else:
        msg = "Unable to determine boolean from " + type(input).__name__
        raise ValueError, msg

def cdate(input, doquote=True, dodbfunction=False):
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
        
        >>> print 'SET updated = %s;' % cdate('now()', dodbfunction=True)
        SET updated = now();
    
    """
    
    # Is the value NULL
    if input is None or input == '':
        return 'NULL'
    else:
        if not dodbfunction and not data.isdate(input):
            raise ValueError, 'Value passed is not a valid date.'
        
        if doquote and not dodbfunction:
            input = data.wrap(input, "'")
        
    return input

def cfloat(input):
    """
    Returns a formatted string safe for use in SQL. If None is
    passed, it will return 'NULL' so as to insert a NULL value
    into the database.
    
    B{Todo:}
    I{If True/False is passed should these be
    converted to 1/0 respectively?}
        
    @param input: Float to be cleaned
    @type input: Anything
    @return: Float, or 'NULL'
    
        >>> print 'WHERE field = %s;' % cfloat("45")
        WHERE field = 45.0;
    
    """
    
    # Check if the data passed is really NULL
    if input is None: return 'NULL'
    if input is True or input is False:
        raise ValueError, 'True/False is not valid integer. Convert to 0/1?'
    try:
        if input.upper() == 'NULL' or input == '': return 'NULL'
    except:
        pass
    
    try:
        return float(input)
    except:
        raise ValueError, 'Value passed cannot be safely stored as float'

def cint(input):
    """
    Returns a formatted string safe for use in SQL. If None is
    passed, it will return 'NULL' so as to insert a NULL value
    into the database.
    
    B{Todo:}
    I{If True/False is passed should these be
    converted to 1/0 respectively?}  
      
    @param input: Integer to be cleaned
    @type input: Anything
    @return: Integer, or 'NULL'
    
        >>> print 'WHERE field = %s;' % cint("45")
        WHERE field = 45;
    
    """
    
    # Check if the data passed is really NULL
    if input is None: return 'NULL'
    if input is True or input is False:
        raise ValueError, 'True/False is not valid integer. Convert to 0/1?'
    try:
        if input.upper() == 'NULL' or input == '': return 'NULL'
    except:
        pass
    
    try:
        return int(input)
    except:
        msg = 'Value passed cannot be safely stored as int: ' + str(input)
        raise ValueError, msg

def cstr(input, doquote=True, doescape=True):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it will
    return 'NULL' so as to insert a NULL value into the database. Single
    quotes will be escaped.
    
    B{Todo:}
    I{This function needs to support mssql's annoying single quote padding
    style too.}
    
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
    
    # Is the value NULL
    if input is None: return 'NULL'
    
    try:
        input = str(input)
        if input.upper() == 'NULL': return 'NULL'
    except:
        pass
    
    if not data.isstr(input):
        print 'Invalid string:', input
        raise ValueError, "Value is not a string."
    
    # Is the value an empty string
    if input == '':
        return "''"
    
    if doescape:
        escape = {"'":"''", "\\":"\\\\"}
        input = data.replace_all(escape, input)

    if doquote:
        input = data.wrap(input, "'")
    return input

def ctags(input):
    """
    Returns a string safe for use in a sql statement
    @param: input
    @type input: Anything
    @return: 'NULL', or input string
    
        >>> print ctags('')
        NULL
    """
    if input == '':
        return 'NULL'
    
    tags = data.str2tags(input)
    tags = data.tags2str(tags)
    return "'%s'" % tags.lower()

def empty2null(input):
    """
    Returns NULL if an empty string is passed, else returns the input string.
    @param: input
    @type input: Anything
    @return: 'NULL', or input string
    
        >>> print empty2null('')
        NULL
    """
    if input == '':
        return 'NULL'
    else:
        return input
