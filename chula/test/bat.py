"""Class for use with Basic Acceptance Testing"""

# Python imports
from urllib import urlencode
import os
import unittest

# Third party imports
import httplib2

# Chula imports
from chula import collection

PORT = os.environ.get('CHULA_TEST_PORT', 8090)

class Bat(unittest.TestCase):
    def response(self, request):
        resp, content = request
        retval = collection.Collection()
        retval.data = content
        retval.status = int(resp.get('status'))
        retval.headers = resp
        return retval

    def request(self, url):
        return self.get(url)

    def get(self, url):
        http = httplib2.Http()
        return self.response(http.request(self.url(url), 'GET'))

    def post(self, url, data):
        http = httplib2.Http()
        data = urlencode(data)
        return self.response(http.request(self.url(url), 'POST', data))

    def put(self, url, body, headers=None):
        http = httplib2.Http()
        headers = headers or {'content-type':'text/plain'}
        resp = http.request(self.url(url), 'PUT', body=body, headers=headers)
        return self.response(resp)

    def delete(self, url, body, headers=None):
        http = httplib2.Http()
        headers = headers or {'content-type':'text/plain'}
        resp = http.request(self.url(url), 'DELETE', body=body, headers=headers)
        return self.response(resp)

    def url(self, url):
        return 'http://localhost:%s' % PORT + url
