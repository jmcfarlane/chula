"""Base message queue object"""

import sqlite3

from chula import collection, data, db, error
from chula.queue import messages

class Message(collection.Collection):
    def __init__(self, msg=None):
        self.created = None
        self.id = None
        self.inprocess = False
        self.message = None
        self.name = None
        self.processed = False
        self.type = None
        self.updated = None

        self.fill(msg)

    def fill(self, msg):
        if not msg is None:
            if isinstance(msg, dict):
                pass

            for key in self.keys():
                self[key] = msg[key]

            # Enforce attribute types
            self.id = int(self.id)
            self.created = data.str2date(self.created)
            self.updated = data.str2date(self.updated)
            self.inprocess = data.str2bool(self.inprocess)
            self.processed = data.str2bool(self.processed)

    def to_sql(self):
        msg = collection.Collection()
        msg.created = db.cdate(self.created)
        msg.id = db.cint(self.id)
        msg.message = db.cstr(self.message)
        msg.name = db.cstr(self.name)
        msg.type = db.cstr(self.type)
        msg.updated = db.cdate(self.updated)

        # Sqlite needs quoted dates, so treat as strings
        msg.inprocess = db.cstr(self.inprocess)
        msg.processed = db.cstr(self.processed)

        if self.id is None:
            sql = """
                INSERT INTO messages(
                    created,
                    message,
                    name,
                    type
                )
                VALUES(
                    datetime(),
                    %(message)s,
                    %(name)s,
                    %(type)s
                );
                """ % msg
        else:
            sql = """
                UPDATE messages SET
                    name = %(name)s,
                    message = %(message)s,
                    updated = datetime(),
                    inprocess = %(inprocess)s,
                    processed = %(processed)s,
                    type = %(type)s
                WHERE id = %(id)s;
                """ % msg
        
        return sql

class MessageFactory(object):
    def __new__(self, msg):
        if isinstance(msg, basestring):
            mtype = msg
            msg = None
        elif isinstance(msg, sqlite3.Row):
            mtype = msg['type']
        elif isinstance(msg, Message):
            mtype = msg.type
        elif isinstance(msg, dict):
            mtype = msg['type']
        else:
            msg = 'Invalid message: %s' % msg
            raise Exception(msg)

        if mtype == 'email':
            from chula.queue.messages import email as message
        else:
            msg = 'Invalid message type: %s' % mtype
            raise Exception(msg)

        return message.Message(msg)

class CannotPurgeUnprocessedError(error.ChulaException):
    """
    Exception indicating that the message was not marked as having
    been processed, thus cannot be purged from the queue
    """

    def msg(self):
        return "Unable to purge an unprocessed message"
