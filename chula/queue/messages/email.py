"""
Chula email message object
"""

from chula import collection
from chula.queue.messages import message

class Message(message.Message):
    def __init__(self, msg):
        super(Message, self).__init__(msg)
        self.type = 'email'
        self.message = Contract()

    def process(self):
        return 'The email processing is not implemented yet :/'

    def validate(self):
        for key, value in self.message.iteritems():
            if value == collection.UNSET:
                msg = 'Required message attribute not specified: %s' % key
                raise KeyError(msg)

class Contract(collection.RestrictedCollection):
    def __validkeys__(self):
        """
        Email message body to force the required attributes
        """

        return ('body', 'from_addy', 'smtp', 'to_addy')


    def __defaults__(self):
        self.body = collection.UNSET
        self.smtp = collection.UNSET
        self.from_addy = collection.UNSET
        self.to_addy = collection.UNSET
