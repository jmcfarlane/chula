"""
Chula email message object
"""

from chula import collection, mail
from chula.queue.messages import message

class Message(message.Message):
    def __init__(self, msg):
        super(Message, self).__init__(msg)
        self.type = 'email'

    def fill(self, msg):
        super(Message, self).fill(msg)
        self.message = Contract()

        # Update the contract
        if not msg is None:
            if not msg['message'] is None:
                for key, value in msg['message'].iteritems():
                    self.message[key] = value

    def process(self):
        email = mail.Mail(self.message.smtp)
        email.from_addy = self.message.from_addy
        email.to_addy = self.message.to_addy
        email.body = self.message.body
        email.subject = self.message.subject

        try:
            email.send()
            return 'Mail Sent'
        except Exception, er:
            return er

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

        return ('body',
                'from_addy',
                'reply_to_addy',
                'smtp',
                'subject',
                'to_addy')

    def __defaults__(self):
        self.body = collection.UNSET
        self.from_addy = collection.UNSET
        self.reply_to_addy = None
        self.smtp = collection.UNSET
        self.subject = collection.UNSET
        self.to_addy = collection.UNSET
