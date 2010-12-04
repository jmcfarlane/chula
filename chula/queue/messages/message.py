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
        self.type = '%s.%s' % (self.__class__.__module__,
                               self.__class__.__name__)

        if not msg is None:
            # Fill from the decoded message values
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

    def validate(self):
        pass

class MessageFactory(object):
    """
    Transform the passed object into it's native type
    """

    def __new__(self, msg):
        """
        Construct a new message of any subclass of Message()

        @param msg: Message to be created
        @type msg: file or dict
        @return: chula.queue.messages.message.Message or subclass of
        """

        if isinstance(msg, file):
            msg = Message.decode(''.join(msg.readlines()))

            # Currently not persisting "inprocess" to the file so go
            # by the name of the actual file, not it's contents
            if str(file.name).endswith('.inprocess'):
                msg['inprocess'] = True
        elif isinstance(msg, dict):
            pass
        else:
            msg = 'Invalid message: %s' % msg
            raise Exception(msg)
            
        try:
            # Pull out the exact type of message and import the module
            module_path, class_name = msg['type'].rsplit('.', 1)
            module = __import__(module_path, globals(), locals(), [class_name])

            # Instantiate an instance of the actual type (subclass of Message)
            msg = module.Message(msg)
        except Exception, ex:
            msg = 'Error detail: %s' % ex
            raise InvalidMessageEncodingError(msg)

        # Some sanity checking
        if not isinstance(msg, Message):
            msg = '[%s] must subclass chula.queue.messages.Message' % msg
            raise Exception(msg)
        else:
            return msg

class IOErrorWhenPurgingProcessedMessage(error.ChulaException):
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
