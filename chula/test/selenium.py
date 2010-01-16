import os
import socket
import sys
import time
import unittest

from chula.vendor import selenium as upstream

KEY_ENTER = '10'
UNSET = 'UNSET'

class TestCase(unittest.TestCase):
    def __init__(self, methodName):
        super(TestCase, self).__init__(methodName)

        # Member variables
        self.browser = '*firefox'
        self.max_wait = 15 * 1000
        self.remote_control_port = 4444
        self.remote_control = 'localhost'
        self.speed = 0
        self.target = 'http://localhost'

        # Fill any attributes from the environment
        for key in os.environ:
            if getattr(self, key, None) is UNSET:
                setattr(self, key, os.environ[key])

        # Cast a few types
        self.speed = int(self.speed)
        self.max_wait = int(self.max_wait)

    def setUp(self):
        self.selenium = upstream.selenium(self.remote_control,
                                          self.remote_control_port,
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
