"""
Chula message queue daemon
"""

import os
import socket
import sys
import thread
import time

from chula import json
from chula.queue import mqueue
from chula.queue.messages import message

class MessageQueueServer(object):
    def __init__(self, config):
        self.config = config
        self.poll = 30

    def producer(self, client):
        chars_left = 1
        msg = ['']
        msg_length = None

        for x in xrange(1000):
            chunk = client.recv(chars_left)
            if chunk == '':
                client.send('OK ')
                break

            if msg_length is None:
                if chunk == ':':
                    try:
                        msg_length = int(msg.pop())
                        chars_left = msg_length
                        continue
                    except ValueError:
                        client.send('BAD')
                        break
                else:
                    msg[0] += chunk
            else:
                if chars_left > 1:
                    chars_left -= len(chunk)
                msg.append(chunk)

        # Combine the chunks
        msg = ''.join(msg)
        print '[%s]' % msg

        # Decode the data
        msg = json.decode(msg)
        msg = message.MessageFactory(msg)
        
        # Create an instance of the queue and add to it
        queue = self.queue()
        queue.add(msg)
        queue.close()

        try:
            client.shutdown(0)
        except socket.error:
            pass
        client.close()

    def consumer(self):
        while True:
            queue = self.queue()
            msg = queue.pop()
            if not msg is None:
                print msg
            queue.close()
            print 'Queue polled for messages'
            time.sleep(self.poll)

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.config.mqueue_host, self.config.mqueue_port))
        s.listen(5)

        # Startup the consumer thread
        thread.start_new_thread(self.consumer, ())

        # Serve forever
        while True:
            try:
                (clientsocket, address) = s.accept()
                thread.start_new_thread(self.producer, (clientsocket,))
            except KeyboardInterrupt:
                break

        s.shutdown(0)
        s.close()

    def queue(self):
        return mqueue.MessageQueue(self.config)

# Testing
if __name__ == '__main__':
    print 'Running with pid: %s' % os.getpid()
    daemon = sys.argv[0].rsplit('/', 1)[-1]
    pid = open('/tmp/%s.pid' % daemon, 'w')
    pid.write(str(os.getpid()))
    pid.close()

    from chula import config
    config = config.Config()
    server = MessageQueueServer(config)
    server.start()
