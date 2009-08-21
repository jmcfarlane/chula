"""Class for use with Basic Acceptance Testing"""

import os
import signal
import subprocess
import time
import unittest
import urllib2

class Bat(unittest.TestCase):
    def setUp(self):
        self.server = subprocess.Popen(['./apps/basic/webserver'],
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        time.sleep(0.5)

    def tearDown(self):
        os.kill(self.server.pid, signal.SIGTERM)

    def request(self, url):
        if not url.startswith('http://'):
            url = 'http://localhost:8080' + url

        return urllib2.urlopen(url).read()
