"""
Chula echo message object
"""

from chula.queue.messages import message

class Message(message.Message):
    def process(self):
        return self.message

if __name__ == '__main__':
    from chula.queue.messages.echo import Message
    from chula.queue.tester import Tester

    msg = Message() 
    msg.message = 'This is a test message'

    tester = Tester()
    tester.test(msg)

