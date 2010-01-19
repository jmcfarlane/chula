"""
Chula message queue daemon
"""

from __future__ import with_statement
import datetime
import os
import socket
import sys
import thread
import time

from chula import json, logger, system
from chula.queue import mqueue
from chula.queue.messages import message

class MessageQueueServer(object):
    """
    Multithreaded server for processing messages in an asynchronous
    fashion.  Communication with the server happens via TCP sockets.
    """

    def __init__(self, config):
        """
        @param config: Chula configuration
        @type config: chula.config.Config
        """

        self.config = config
        self.debug = True
        self.log = logger.Logger(config).logger('chula.queue.server')
        self.pid_file = os.path.join(self.config.mqueue_db, 'server.pid')
        self.queue = mqueue.MessageQueue(self.config)
        self.system = system.System()
        self.thread_count = 0
        self.thread_max = self.system.procs + 1

    def worker(self):
        """
        Method to process messages in the queue.  The number of worker
        threads that are spawned at startup are configurable.
        """

        thread_id = thread.get_ident()
        self.log.debug('Worker thread started: %s' % thread_id) 
        while True:
            msg = self.queue.get()
            try:
                result = msg.process()
                self.queue.persist_result(msg, result)
                self.queue.purge(msg)
            except Exception, ex:
                self.queue.purge(msg, ex)

            self.log.debug('%s was processed' % msg.name)
            if self.debug:
                print '%s processed by: %s' % (msg.name, thread_id)

    def receive_message(self, client):
        """
        Receive a message from a chula.queue.client or anything else
        really.

        @param client: TCP Socket
        @type client: socket._socketobject
        """

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
        """
        Start the mqueue server
        """

        # Create a pid file
        pid = open(self.pid_file, 'w')
        pid.write(str(os.getpid()))
        pid.close()

        # Listen on the specified port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.config.mqueue_host, self.config.mqueue_port))
        s.listen(5)

        # Startup worker threads
        for t in xrange(self.thread_max):
            thread.start_new_thread(self.worker, ())

        # Before starting the server add any unprocessed msgs to the queue
        for msg in self.queue.unprocessed_messages():
            info = 'Found message out of band, adding to queue: %s'
            self.log.debug(info % msg)
            self.queue.add(msg)

        # Serve forever
        while True:
            try:
                (clientsocket, address) = s.accept()
                thread.start_new_thread(self.receive_message, (clientsocket,))
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
    server = MessageQueueServer(config)
    server.start()
