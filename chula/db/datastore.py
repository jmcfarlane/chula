"""
Chula datastore object, provides consistent access to all supported
database engines
"""

import re

# Loading ourselves before third party is bad, but we need to be able
# to raise our own exception if things go wrong
from chula import error, data

class DataStoreFactory(object):
    """
    The Database class creates an instance of a supported database
    engine (aka datastore)
    """
    
    def __new__(cls, conn, *args, **kwargs):
        """
        Creates an instance of a DataStore class.
        
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
        
        >>> conn = DataStoreFactory('pg:chula@localhost/chula_test', 'passwd')
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
        
        try:
            parts = conn.split(':')
            if len(parts) > 1:
                engine = parts[0]
                uri = ':'.join(parts[1:])
            else:
                raise error.MalformedConnectionStringError
        except AttributeError:
            raise error.MalformedConnectionStringError(conn)

        if engine == 'pg':
            from chula.db.engines import postgresql as engine
        elif engine == 'couchdb':
            from chula.db.engines import couch as engine
        elif engine == 'sqlite':
            from chula.db.engines import sqlite as engine
        else:
            raise error.UnsupportedDatabaseEngineError(engine)

        # Return a database engine instance
        return engine.DataStore(uri, *args, **kwargs)

