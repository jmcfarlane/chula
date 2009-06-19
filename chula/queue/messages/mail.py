"""
Chula email message object
"""

from chula import collection
from chula.mail import Mail
from chula.queue.messages import message

class Message(message.Message):
    def fill(self, msg):
        super(Message, self).fill(msg)
        self.message = Contract()

        # Update the contract
        if not msg is None:
            if not msg['message'] is None:
                for key, value in msg['message'].iteritems():
                    self.message[key] = value

    def process(self):
        email = Mail(self.message.smtp)
        email.from_addy = self.message.from_addy
        email.to_addy = self.message.to_addy
        email.body = self.message.body
        email.subject = self.message.subject

        try:
            email.send()
            return 'Mail Sent'
        except:
            raise

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

if __name__ == '__main__':
    from chula.queue.messages.mail import Message
    from chula.queue.tester import Tester

    msg = Message() 
    msg.message.body = 'Hello world'
    msg.message.subject = 'Testing message queue with email message'
    msg.message.from_addy = 'john.mcfarlane+chula@gmail.com'
    msg.message.to_addy = msg.message.from_addy
    msg.message.smtp = 'smtp.comcast.net'

    tester = Tester()
    tester.test(msg)
