import os
import socket
import sys
import time
import unittest

from chula.vendor import selenium as upstream

KEY_ENTER = '10'

class TestCase(unittest.TestCase):
    def __init__(self, methodName):
        super(TestCase, self).__init__(methodName)

        # Member variables
        self.browser = '*firefox'
        self.max_wait = 15 * 1000
        self.rc = 'localhost'
        self.rc_port = 4444
        self.speed = 0
        self.target = 'http://localhost'

        # Fill any attributes from the environment
        for key, value in os.environ.iteritems():
            setattr(self, key, value)

        # Cast a few types
        self.max_wait = int(self.max_wait)
        self.rc_port = int(self.rc_port)
        self.speed = int(self.speed)

    def setUp(self):
        self.selenium = upstream.selenium(self.rc,
                                          self.rc_port,
                                          self.browser,
                                          self.target)

        # Create a shorthand alias
        self.s = self.selenium

        # Start a session on the remote control, slow things down a little
        self.selenium.start()
        self.selenium.set_speed(int(self.speed))

    def tearDown(self):
        self.selenium.stop()

    def wait(self):
        self.selenium.wait_for_page_to_load(self.max_wait)
