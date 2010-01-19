"""Class for use with Basic Acceptance Testing"""

import os
import signal
import subprocess
import time
import unittest
import urllib2

from chula import collection

#class RedirectHandler(urllib2.HTTPRedirectHandler):
#    def http_error_301(self, req, fp, code, msg, headers):
#        upstream = urllib2.HTTPRedirectHandler.http_error_301
#        result = upstream(self, req, fp, code, msg, headers)
#        result.code = code
#        return result
#
#    def http_error_302(self, req, fp, code, msg, headers):
#        upstream = urllib2.HTTPRedirectHandler.http_error_302  
#        result = upstream(self, req, fp, code, msg, headers)
#        result.code = code
#        return result

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

        #opener = urllib2.build_opener(RedirectHandler())
        #response = opener.open(url)

        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, ex:
            response = ex
        except urllib2.URLError, ex:
            response = ex

        retval = collection.Collection()
        retval.data = response.read()
        retval.status = response.code
        retval.headers = response.info().headers

        return retval
