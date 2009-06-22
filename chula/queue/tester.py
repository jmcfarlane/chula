"""
Module for sending test messages thru the queue
"""

import time

from chula.config import Config
from chula.queue import client

class Tester(object):
    def __init__(self, config=None, debug=True, wait=500):
        self.client = client.MessageQueueClient(Config())
        self.debug = debug
        self.wait = wait

    def test(self, msg):
        id = self.client.add(msg)
        print 'Message added to queue:', id

        if self.debug:
            self.get_response(id)

    def get_response(self, id):
        print '>>> Waiting for response...'
        for x in xrange(self.wait):
            time.sleep(0.001)
            response = self.client.fetch(id)
            if not response is None:
                print '>>> Response:', response
                break

        if response is None:
            print ">>> No response after %sms" % self.wait
