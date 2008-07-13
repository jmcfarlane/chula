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
        self.conn = sqlite3.connect(uri)
