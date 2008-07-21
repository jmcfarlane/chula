"""
TCP client for the Chula message queue daemon
"""

import socket

class MessageQueueClient(object):
    def __init__(self, config):
        pass

    def add(self, msg):
        msg = self.encode(msg)
        msg_length = len(msg)
        chars_left = msg_length

        self.connect()
        while chars_left > 0:
            sent = self.socket.send(msg)
            chars_left -= sent
            print msg_length, sent

        self.close()

    def encode(self, msg):
        msg = '%s:%s' % (len(msg), msg)
        return msg

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', 8080))

    def close(self):
        #self.socket.shutdown()
        self.socket.close()

client = MessageQueueClient('')
client.add('foo akdfalksd fkalsjd flkad fklafj ksajf kalsdf')
