"""Simple message queue object"""

from chula import data, db
from chula.queue import base

class Message(base.QueueObject):
    def to_sql(self):
        self.name = db.cstr(self.name)
        sql = """
            INSERT INTO messages(timestamp, name)
            VALUES(datetime(), %(name)s);
            """ % self
        
        return sql

    def pop(self):
        pass

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
                timestamp DATE,
                name TEXT,
                processed INTEGER DEFAULT 0
            )
            """

        self.persist(sql)

    def delete_by_id(self, id):
        sql = 'DELETE FROM messages WHERE id = %s;' % db.cint(id)
        self.persist(sql)

    def pop(self):
        sql = """SELECT * FROM messages
            ORDER BY id ASC limit 1;
            """

        msg = Message()
        row = self.cursor.execute(sql).fetchone()
        if row is None:
            return row

        # We have a message
        for key in msg.keys():
            msg[key] = row[key]

        # Set non string types
        msg.id = int(msg.id)
        msg.timestamp = data.str2date(msg.timestamp)
        msg.processed = data.str2bool(msg.processed)

        # Remove from the queue
        self.delete_by_id(msg.id)

        return msg

