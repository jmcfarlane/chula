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
    
    def __init__(self, str_conn, str_passwd=''):
        """
        Datastore constructor. Creates an instance of the Datastore class.
        
        The connection string is a tuple with the following values in order:
            1. Database type B{(Currently the only supported option is: pg)}
            2. Username
            3. Host
            4. Database name
            
            eg: pg:username@server/databasename
        
        @param str_conn: Connection string
        @type str_conn: String
        @param str_passwd: Database password
        @type str_passwd: String
        @return: Instance
        
            >>> obj_conn = Datastore('pg:chula@localhost/chulatest', 'password')
            
        """
        
        # TODO: Add regex check on the connection string
        tup_db = (str_conn[str_conn.find('@')+1:str_conn.find('/')],
                  str_conn[str_conn.find('/')+1:],
                  str_conn[str_conn.find(':')+1:str_conn.find('@')],
                  str_passwd)
        
        self.conn = psycopg2.connect(
            ('host=%s dbname=%s user=%s password=%s') % (tup_db)
        )
        
    def set_isolation(self, int_level=1):
        """
        Toggle the isolation level. Here are the available
        isolation levels:
            - 0 = No isolation
            - 1 = READ COMMITTED (the default)
            - 3 = SERIALIZABLE
        
        @param int_level: Isolation level
        @type int_level: Integer
        @return: Nothing
        """
        
        self.conn.set_isolation_level(int_level)
    
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
    
    def cursor(self, str_type='dict'):
        """
        Create database cursor.
        
        @return: Instance
        """
        if str_type == 'tuple':
            return self.conn.cursor(cursor_factory=Cursor)
        else:
            return self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    def execute(self, str_sql):
        """
        Execute I{SQL} statement.
        
        @param str_sql: SQL statement to execute
        @type str_sql: String
        @return: Cursor
        
            >>> obj_conn = Datastore('pg:chula@localhost/chulatest', 'password')
            >>> obj_rs = obj_conn.cursor()
            >>> obj_rs.execute("SELECT * FROM cars;")
            >>> obj_rs.execute("INSERT INTO cars(make, model) VALUES('Honda', 'Civic');")
            >>> obj_conn.commit()
            
        """
        
        print "I think this function needs to be depricated?"
        str_temp = str_sql.upper()
        print str_temp.find('DELETE')
        if str_temp.find('UPDATE') >= 0 or str_temp.find('DELETE') >= 0:
            if str_temp.find('WHERE') <= 0:
                raise Exception, 'Dummy, please try adding a WHERE clause!'
            
        return self.cursor().execute(str_sql)

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
    
def clean_bool(str_input):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it will
    return 'NULL' so as to insert a NULL value into the database.
    
    @param str_input: String to be cleaned
    @type str_input: String
    @return: String I{TRUE/FALSE}, or 'NULL'
    
        >>> print 'SET active = %s;' % clean_bool(True)
        SET active = TRUE;
    
    """
    
    if str_input is None or str_input == '': return 'NULL'
    
    if isinstance(str_input, str):
        list_true = [1, 'on', 't', 'true', 'y', 'yes', '1']
        list_false = [0, 'off', 'f', 'false', 'n', 'no', '0']
        str_input = str_input.lower()
    else:
        list_true = [True]
        list_false = [False]
        
    if str_input in list_true:
        return 'TRUE'
    elif str_input in list_false:
        return 'FALSE'
    else:
        raise ValueError, "Unable to determine boolean from " + type(str_input).__name__

def clean_date(str_input, bool_quote=True, bool_dbfunction=False):
    """
    Returns a formatted string safe for use in SQL. If None or an empty
    string is passed, it will return 'NULL' so as to insert a NULL value
    into the database.
    
    B{Todo:}
    I{This function needs to be able to receive datetime.datetime types too.}
    
    @param str_input: Date to be cleaned
    @type str_input: String
    @return: String, or 'NULL'
    
        >>> print 'SET date_updated = %s;' % clean_date('1/1/2005')
        SET date_updated = '1/1/2005';
        
        >>> print 'SET date_updated = %s;' % clean_date('now()', bool_dbfunction=True)
        SET date_updated = now();
    
    """
    
    # Is the value NULL
    if str_input is None or str_input == '':
        return 'NULL'
    else:
        if not bool_dbfunction and not data.isdate(str_input):
            print 'Invalid date:', str_input
            raise ValueError, 'Value passed is not a valid date.'
        
        if bool_quote and not bool_dbfunction:
            str_input = data.str_wrap(str_input, "'")
        
    return str_input

def clean_float(str_input):
    """
    Returns a formatted string safe for use in SQL. If None is
    passed, it will return 'NULL' so as to insert a NULL value
    into the database.
    
    B{Todo:}
    I{If True/False is passed should these be
    converted to 1/0 respectively?}
        
    @param str_input: Float to be cleaned
    @type str_input: Anything
    @return: Float, or 'NULL'
    
        >>> print 'WHERE field = %s;' % clean_float("45")
        WHERE field = 45.0;
    
    """
    
    # Check if the data passed is really NULL
    if str_input is None: return 'NULL'
    if str_input is True or str_input is False:
        raise ValueError, 'True/False is not valid integer. Convert to 0/1?'
    try:
        if str_input.upper() == 'NULL' or str_input == '': return 'NULL'
    except:
        pass
    
    try:
        return float(str_input)
    except:
        print "Invalid float:", str_input
        raise ValueError, 'Value passed cannot be safely stored as float'

def clean_int(str_input):
    """
    Returns a formatted string safe for use in SQL. If None is
    passed, it will return 'NULL' so as to insert a NULL value
    into the database.
    
    B{Todo:}
    I{If True/False is passed should these be
    converted to 1/0 respectively?}  
      
    @param str_input: Integer to be cleaned
    @type str_input: Anything
    @return: Integer, or 'NULL'
    
        >>> print 'WHERE field = %s;' % clean_int("45")
        WHERE field = 45;
    
    """
    
    # Check if the data passed is really NULL
    if str_input is None: return 'NULL'
    if str_input is True or str_input is False:
        raise ValueError, 'True/False is not valid integer. Convert to 0/1?'
    try:
        if str_input.upper() == 'NULL' or str_input == '': return 'NULL'
    except:
        pass
    
    try:
        return int(str_input)
    except:
        print "Invalid int:", str_input
        raise ValueError, 'Value passed cannot be safely stored as int: ' + str(str_input)

def clean_str(str_input, bool_quote=True, bool_escape=True):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it will
    return 'NULL' so as to insert a NULL value into the database. Single
    quotes will be escaped.
    
    B{Todo:}
    I{This function needs to support mssql's annoying single quote padding
    style too.}
    
    @param str_input: String to be cleaned
    @type str_input: String
    @param bool_quote: I{OPTIONAL}: Wrapped in single quotes, defaults to B{True}
    @type bool_quote: Boolean
    @param bool_escape: I{OPTIONAL}: Escape single quotes, defaults to B{True}
    @type bool_escape: Boolean
    @return: String, or 'NULL'
    
        >>> print 'SET description = %s;' % clean_str("I don't")
        SET description = 'I don''t';
        >>> print 'SET date_now = %s;' % clean_str("CURRENT_TIME", bool_quote=False)
        SET date_now = CURRENT_TIME;
    
    """
    
    # Is the value NULL
    if str_input is None: return 'NULL'
    
    try:
        str_input = str(str_input)
        if str_input.upper() == 'NULL': return 'NULL'
    except:
        pass
    
    if not data.isstr(str_input):
        print 'Invalid string:', str_input
        raise ValueError, "Value is not a string."
    
    # Is the value an empty string
    if str_input == '':
        return "''"
    
    if bool_escape:
        dict_escape = {"'":"''", "\\":"\\\\"}
        str_input = data.replace_all(dict_escape, str_input)

    if bool_quote:
        str_input = data.str_wrap(str_input, "'")
    return str_input

def clean_tags(str_input):
    """
    Returns a string safe for use in a sql statement
    @param: str_input
    @type str_input: Anything
    @return: 'NULL', or input string
    
        >>> print clean_tags('')
        NULL
    """
    if str_input == '':
        return 'NULL'
    
    list_tags = data.str2tags(str_input)
    str_tags = data.tags2str(list_tags)
    return "'%s'" % str_tags.lower()

def empty2null(str_input):
    """
    Returns NULL if an empty string is passed, else returns the input string.
    @param: str_input
    @type str_input: Anything
    @return: 'NULL', or input string
    
        >>> print empty2null('')
        NULL
    """
    if str_input == '':
        return 'NULL'
    else:
        return str_input
    
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

        
