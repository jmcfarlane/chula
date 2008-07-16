"""Simple message queue object"""

from chula import collection, db, error
from chula.queue import base

class Message(base.QueueObject):
    def to_sql(self):
        msg = collection.Collection()
        msg.id = db.cint(self.id)
        msg.name = db.cstr(self.name)
        msg.created = db.cdate(self.created)
        msg.updated = db.cdate(self.updated)

        # Sqlite needs quoted dates, so treat as strings
        msg.inprocess = db.cstr(self.inprocess)
        msg.processed = db.cstr(self.processed)

        if self.id is None:
            sql = """
                INSERT INTO messages(created, name)
                VALUES(datetime(), %(name)s);
                """ % msg
        else:
            sql = """
                UPDATE messages SET
                    name = %(name)s,
                    updated = datetime(),
                    inprocess = %(inprocess)s,
                    processed = %(processed)s
                WHERE id = %(id)s;
                """ % msg
        
        return sql

class MessageQueue(base.Queue):
    def add(self, name):
        msg = Message()
        msg.name = name
        self.persist(msg)

    def schema_exists(self):
        tables = self.fetch_schema()
        for table in tables:
            if table['name'] == 'messages':
                return True

        return False

    def create_schema(self):
        sql = """
            CREATE TABLE messages(
                id INTEGER PRIMARY KEY,
                created DATE,
                updated DATE,
                name TEXT,
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
        msg = Message(msg)
        
        return msg

    def pop(self):
        sql = """SELECT * FROM messages
            ORDER BY id ASC limit 1;
            """

        msg = Message()
        row = self.cursor.execute(sql).fetchone()
        if row is None:
            return row

        # We have a message
        msg = Message(row)
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
            raise CannotPurgeUnprocessedError(msg)

class CannotPurgeUnprocessedError(error.ChulaException):
    """
    Exception indicating that the message was not marked as having
    been processed, thus cannot be purged from the queue
    """

    def msg(self):
        return "Unable to purge an unprocessed messagage"
