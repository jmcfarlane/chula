"""Chula Sqlite datastore object"""

try:
    import sqlite3
except:
    raise error.MissingDependencyError('sqlite3')

from chula.db.engines import engine

def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d

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
            self.conn.row_factory = _dict_factory

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
            - EXCLUSIVE = ?
        
        @param level: Isolation level
        @type level: str
        """
        
        self.conn.isolation_level = level
    
