"""Base message queue object"""

import datetime
import thread

from chula import collection, data, error, json
from chula.queue import messages

class Message(collection.Collection):
    def __init__(self, msg=None):
        self.created = None
        self.id = thread.get_ident()
        self.inprocess = False
        self.message = None
        self.name = self.msg_name()
        self.processed = False
        self.type = None
        self.updated = None

        self.fill(msg)

    def msg_name(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        return '%s.%s.msg' % (now, self.id)

    @staticmethod
    def decode(msg):
        return json.decode(msg)

    def encode(self):
        return json.encode(self)

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

class MessageFactory(object):
    def __new__(self, msg):
        if isinstance(msg, basestring):
            mtype = msg
            msg = None
        elif isinstance(msg, Message):
            mtype = msg.type
        elif isinstance(msg, dict):
            mtype = msg['type']
        elif isinstance(msg, file):
            msg = ''.join(msg.readlines())
            msg = Message.decode(msg)
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
