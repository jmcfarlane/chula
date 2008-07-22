"""Base message queue object"""

import sqlite3

from chula import collection, data, db, error
from chula.queue import messages

class Message(collection.Collection):
    def __init__(self, msg=None):
        self.id = None
        self.message = None
        self.name = None
        self.inprocess = False
        self.processed = False
        self.type = None
        self.created = None
        self.updated = None

        # Fill if data provided
        if not msg is None:
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
        msg.id = db.cint(self.id)
        msg.name = db.cstr(self.name)
        msg.message = db.cstr(self.message)
        msg.created = db.cdate(self.created)
        msg.updated = db.cdate(self.updated)
        msg.type = db.cstr(self.type)

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
            message_type = msg
            msg = None
        elif isinstance(msg, sqlite3.Row):
            message_type = msg['type']
        elif isinstance(msg, Message):
            message_type = msg.type
        else:
            msg = 'Invalid message: %s' % msg
            raise Exception(msg)

        if message_type == 'email':
            from chula.queue.messages import email as message
        else:
            msg = 'Invalid message type: %s' % message_type
            raise Exception(msg)

        return message.Message(msg)

class CannotPurgeUnprocessedError(error.ChulaException):
    """
    Exception indicating that the message was not marked as having
    been processed, thus cannot be purged from the queue
    """

    def msg(self):
        return "Unable to purge an unprocessed message"
