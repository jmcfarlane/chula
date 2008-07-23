"""
CHula email message object
"""

from chula.queue.messages import message

class Message(message.Message):
    def __init__(self, msg):
        super(Message, self).__init__(msg)
        self.type = 'email'
