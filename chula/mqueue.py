"""Simple message queue object"""

from chula.db import datastore

class MessageQueue(object):
    def __init__(self, config, db=None):
        self.conn = None

        if db is None:
            self.db = config.mqueue_db
        else:
            self.db = db

    def close(self):
        self.conn.close()
        
    def connect(self):
        self.conn = datastore.DataStoreFactory(self.db)
