"""
Chula message queue
"""

from chula import collection, db
from chula.db import datastore
from chula.queue.messages import message

class MessageQueue(object):
    def __init__(self, config, db=None):
        if db is None:
            self.db = config.mqueue_db
        else:
            self.db = db

        # Create a connection to the database
        self.conn = datastore.DataStoreFactory(self.db, 'EXCLUSIVE')
        self.cursor = self.conn.cursor()

        # Create the schema if necessary
        if self.schema_exists() is False:
            self.create_schema()

    def add(self, msg):
        self.persist(msg)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def create_schema(self):
        sql = """
            CREATE TABLE messages(
                id INTEGER PRIMARY KEY,
                created DATE,
                updated DATE,
                message TEXT,
                name TEXT,
                type TEXT,
                inprocess TEXT DEFAULT 'False',
                processed TEXT DEFAULT 'False' 
            )
            """

        self.persist(sql)

    def delete_by_id(self, id):
        sql = 'DELETE FROM messages WHERE id = %s;' % db.cint(id)
        self.persist(sql)

    def fetch_by_id(self, id):
        sql = 'SELECT * FROM messages WHERE id = %s;' % db.cint(id)
        self.cursor.execute(sql)
        msg = self.cursor.fetchone()
        msg = message.MessageFactory(msg)
        
        return msg

    def fetch_schema(self):
        sql = 'SELECT * FROM sqlite_master;'
        self.cursor.execute(sql)
        objects = self.cursor.fetchall()

        tables = []
        for obj in objects:
            if obj['type'] == 'table':
                tables.append(obj)

        return tables

    def list(self):
        msgs = []

        sql = 'SELECT * FROM messages ORDER BY id ASC;'
        for msg in self.cursor.execute(sql).fetchall():
            msgs.append(message.MessageFactory(msg))

        return msgs

    def persist(self, obj):
        if isinstance(obj, basestring):
            self.cursor.execute(obj)
        else:
            self.cursor.execute(obj.to_sql())

        self.conn.commit()

    def pop(self):
        sql = """
            SELECT * FROM messages
            WHERE
                inprocess = 'False' AND
                processed = 'False'
            ORDER BY id ASC limit 1;
            """

        row = self.cursor.execute(sql).fetchone()
        if row is None:
            return row

        # We have a message
        msg = message.MessageFactory(row)
        msg.inprocess = True

        # Persist
        self.persist(msg)

        return msg

    def purge(self, msg):
        inqueue = self.fetch_by_id(msg.id)
        if inqueue.inprocess is True:
            self.delete_by_id(msg.id)
        else:
            msg = 'The messagage was not marked as being processed'
            raise message.CannotPurgeUnprocessedError(msg)

    def schema_exists(self):
        tables = self.fetch_schema()
        for table in tables:
            if table['name'] == 'messages':
                return True

        return False
