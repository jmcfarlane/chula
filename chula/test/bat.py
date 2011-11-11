

# Python imports
import urllib
import os
import unittest

# Third party imports
import httplib2

# Chula imports
from chula import collection

PORT = os.environ.get('CHULA_TEST_PORT', 8090)
PROVIDER = os.environ.get('CHULA_TEST_PROVIDER', 'builtin')

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
        # For some reason chula is responding oddly to http POST
        # variables when requested by httplib2.  It responds fine with
        # urllib or curl.  Using urllib for a bit longer (for this
        # method only.
        data = urllib.urlencode(data)
        response = urllib.urlopen(self.url(url), data)
        retval = collection.Collection()
        retval.data = response.read()
        retval.status = response.code
        retval.headers = response.info().headers
        return retval

    def post_file(self, url, body):
        http = httplib2.Http()
        return self.response(http.request(self.url(url), 'POST', body=body))

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
