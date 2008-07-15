"""Chula Sqlite datastore object"""

try:
    import sqlite3
except:
    raise error.MissingDependencyError('sqlite3')

from chula.db.engines import engine

class DataStore(engine.Engine):
    """
    Sqlite engine class
    """
    
    def __init__(self, uri):
        super(DataStore, self).__init__()

        if uri == 'memory':
            uri = ':memory:'

        self.conn = sqlite3.connect(uri)

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
            - None = Autocommit mode (the default)
            - IMMEDIATE = ?
            - EXCLUSIVE = Prevents anyone else from reading/writing
        
        @param level: Isolation level
        @type level: str
        """
        
        self.conn.isolation_level = level
    
