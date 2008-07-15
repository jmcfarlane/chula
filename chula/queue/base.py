"""
Base queue objects
"""

from chula import collection
from chula.db import datastore

class QueueObject(collection.Collection):
    def __init__(self):
        self.id = None
        self.name = None
        self.processed = 0
        self.timestamp = None

    def to_sql(self):
        msg = 'Please overload the to_sql() method'
        raise NotImplementedError(msg)

class Queue(object):
    def __init__(self, config, db=None):
        self.conn = None

        if db is None:
            self.db = config.mqueue_db
        else:
            self.db = db

        # Create a connection to the database
        self.conn = datastore.DataStoreFactory(self.db)
        self.cursor = self.conn.cursor()

        # Create the schema if necessary
        if self.schema_exists() is False:
            self.create_schema()

    def close(self):
        self.conn.close()

    def schema_exists(self):
        msg = 'Please overload the schema_exists() method'
        raise NotImplementedError(msg)

    def fetch_schema(self):
        sql = 'SELECT * FROM sqlite_master;'
        self.cursor.execute(sql)
        objects = self.cursor.fetchall()

        tables = []
        for obj in objects:
            if obj['type'] == 'table':
                tables.append(obj)

        return tables

    def persist(self, obj):
        if isinstance(obj, basestring):
            self.cursor.execute(obj)
        else:
            self.cursor.execute(obj.to_sql())

        self.conn.commit()

    def pop(self):
        msg = 'Please overload the pop() method'
        raise NotImplementedError(msg)

