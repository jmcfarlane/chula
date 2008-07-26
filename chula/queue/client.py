"""
TCP client for the Chula message queue daemon
"""

import socket

from chula.queue.messages import message

class MessageQueueClient(object):
    def __init__(self, config):
        self.host = config.mqueue_host
        self.port = config.mqueue_port

    def add(self, msg):
        msg = self.encode(msg)
        msg_length = len(msg)
        chars_left = msg_length

        # Connect to the server and sent the message
        self.connect()
        while chars_left > 0:
            sent = self.socket.send(msg)
            chars_left -= sent

        self.close()

    def encode(self, msg):
        msg = message.Message.encode(msg)
        msg = '%s:%s' % (len(msg), msg)
        return msg

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def close(self):
        self.socket.shutdown(0)
        self.socket.close()

# Testing
if __name__ == '__main__':
    from chula import config
    config = config.Config()
    client = MessageQueueClient(config)

    msg = message.MessageFactory('email')
    msg.message = 'I love Lisa'
    client.add(msg)
