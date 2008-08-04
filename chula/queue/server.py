"""
Chula message queue daemon
"""

import datetime
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
        self.poll = self.config.mqueue_poll
        self.queue = mqueue.MessageQueue(self.config)
        self.pid_file = os.path.join(self.config.mqueue_db, 'server.pid')
        self.log_file = os.path.join(self.config.mqueue_db, 'log')

    def consumer(self, msg):
        print ' >>> %s processed by: %s' % (msg.name, thread.get_ident())
        result = msg.process()
        self.queue.persist_result(msg, result)
        self.queue.purge(msg)
        self.log('%s was processed' % msg.name)

    def log(self, msg):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log = open(self.log_file, 'a')
        log.write('%s: %s\n' % (now, msg))
        log.close()

    def poller(self):
        while True:
            msg = self.queue.pop()
            if msg is None:
                time.sleep(self.poll)
            else:
                thread.start_new_thread(self.consumer, (msg, ))

    def producer(self, client):
        chars_left = 1
        msg = ['']
        msg_length = None

        # Consume the message
        while chars_left > 0:
            chunk = client.recv(chars_left)

            # Check if the client closed prematurely
            if chunk == '':
                print 'ERROR: Client socket closed prematurely'
                break

            # Look for the message size
            if msg_length is None:
                if chunk == ':':
                    try:
                        msg_length = int(msg.pop())
                        chars_left = msg_length
                        continue
                    except ValueError:
                        client.sendall('BAD')
                        break
                else:
                    msg[0] += chunk
            else:
                # Once size is known, the rest is the actual message
                if chars_left > 1:
                    chars_left -= len(chunk)
                msg.append(chunk)

        # Combine the chunks
        msg = ''.join(msg)

        # Check to see if this is a message result fetch
        if msg.endswith('.msg'):
            result = self.queue.fetch(msg)
            result = json.encode(result)
            client.sendall(result)
            client.shutdown(0)
            client.close()

            return

        # Decode and add to the queue
        try:
            msg = message.Message.decode(msg)
            msg = message.MessageFactory(msg)
            self.queue.add(msg)
            print '%s added' % msg.name

            # Send a response to the client
            client.sendall(msg.name)
        
        except message.InvalidMessageEncodingError, er:
            print 'Bad message body'
            client.sendall('BAD')
        finally:
            try:
                client.shutdown(0)
                client.close()
            except:
                pass

    def start(self):
        # Create a pid file
        pid = open(self.pid_file, 'w')
        pid.write(str(os.getpid()))
        pid.close()

        # Listen on the specified port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.config.mqueue_host, self.config.mqueue_port))
        s.listen(5)

        # Startup the poller thread
        thread.start_new_thread(self.poller, ())

        # Serve forever
        while True:
            try:
                (clientsocket, address) = s.accept()
                thread.start_new_thread(self.producer, (clientsocket,))
            except KeyboardInterrupt:
                os.remove(self.pid_file)
                print
                print 'Received signal to shutdown...'
                break

        s.shutdown(0)
        s.close()
        
        # Give the socket a second to close
        time.sleep(1)

# Testing
if __name__ == '__main__':
    print 'Running with pid: %s' % os.getpid()

    from chula import config
    config = config.Config()
    config.mqueue_poll = 5
    server = MessageQueueServer(config)
    server.start()
