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
        msg.validate()
        msg = message.Message.encode(msg)
        msg = self.encode(msg)

        # Connect to the server and sent the message
        self.connect()
        sent = self.socket.sendall(msg)

        # Read back the response
        response = []
        while True:
            chunk = self.socket.recv(512)
            response.append(chunk)
            if chunk == '':
                break
            
        self.close()

        return ''.join(response)

    def encode(self, msg):
        msg = '%s:%s' % (len(msg), msg)
        return msg

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def close(self):
        self.socket.shutdown(0)
        self.socket.close()

    def fetch(self, name):
        if name is None:
            return None

        # Connect to the server and sent the message
        self.connect()
        sent = self.socket.sendall(self.encode(name))

        # Read back the response
        response = []
        while True:
            chunk = self.socket.recv(512)
            response.append(chunk)
            if chunk == '':
                break
            
        self.close()

        response = ''.join(response)
        return message.Message.decode(response)
