"""Base message queue object"""

import datetime
import thread

from chula import collection, data, error, json
from chula.queue import messages

class Message(collection.Collection):
    def __init__(self, msg=None):
        now = datetime.datetime.now()
        self.created = now
        self.id = thread.get_ident()
        self.inprocess = False
        self.message = None
        self.name = '%s.%s.msg' % (now.strftime('%Y%m%d%H%M%S'), self.id)
        self.processed = False
        self.type = None
        self.updated = None

        self.fill(msg)

    @staticmethod
    def decode(msg):
        try:
            return json.decode(msg)
        except ValueError, er:
            raise InvalidMessageEncodingError(str(msg))

    def encode(self):
        try:
            mask = '%Y/%m/%d %H:%M:%S'
            self.created = self.created.strftime(mask)
            if not self.updated is None:
                self.updated = self.created.updated(mask)
            return json.encode(self)
        except TypeError, er:
            msg = 'Message is not [json] not encodable: ' + str(self)
            raise TypeError(msg)

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

    def process(self):
        msg = 'Please overload the process() method'
        raise NotImplementedError(msg)

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
            f = msg
            msg = ''.join(f.readlines())
            msg = Message.decode(msg)
            mtype = msg['type']

            # Currently not persisting "inprocess" to the file so go
            # by the name of the actual file, not it's contents
            if f.name.endswith('.inprocess'):
                msg['inprocess'] = True

        else:
            msg = 'Invalid message: %s' % msg
            raise Exception(msg)

        if mtype == 'email':
            from chula.queue.messages import email as message
        elif mtype == 'echo':
            from chula.queue.messages import echo as message
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

class InvalidMessageEncodingError(error.ChulaException):
    """
    Exception indicating that the message is not propery encoded
    """

    def msg(self):
        return "Incorrect encoding, or incomplete message"
