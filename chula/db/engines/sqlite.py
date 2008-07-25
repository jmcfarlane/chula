"""Chula Sqlite datastore object"""

try:
    import sqlite3
except:
    raise error.MissingDependencyError('sqlite3')

from chula import error
from chula.db.engines import engine

ISOLATION_LEVELS = ['DEFERRED',
                    'EXCLUSIVE',
                    'IMMEDIATE',
                    None]

class DataStore(engine.Engine):
    """
    Sqlite engine class
    """
    
    def __init__(self, uri, *args, **kwargs):
        super(DataStore, self).__init__()

        # Handle in memory databases
        if uri == 'memory':
            uri = ':memory:'

        # Handle the initial isolation level
        if 'isolation' in kwargs:
            isolation = kwargs['isolation']
        else:
            isolation = None

        # Handle the initial timeout level
        if 'timeout' in kwargs:
            timeout = kwargs['timeout']
        else:
            timeout = 5

        # Create a database connection
        self.conn = sqlite3.connect(uri,
                                    isolation_level=isolation,
                                    timeout=timeout)

    def cursor(self, type='dict'):
        if type == 'dict':
            self.conn.row_factory = sqlite3.Row

        return super(DataStore, self).cursor()

    def interrupt(self):
        self.conn.interupt()

    def set_isolation(self, level=None):
        """
        Toggle the isolation level. Here are the available
        isolation levels:
            - DEFFERED = ?
            - EXCLUSIVE = Prevents anyone else from reading/writing
            - IMMEDIATE = ?
            - None = Autocommit mode (the default)
        
        @param level: Isolation level
        @type level: str
        """
        
        if level in ISOLATION_LEVELS:
            self.conn.isolation_level = level
        else:
            raise error.InvalidAttributeError(level)
    
