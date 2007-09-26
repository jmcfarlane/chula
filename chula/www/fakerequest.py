"""
Classes to aid in unit testing or anything that needs to simulate a valid
Apache/Mod_python request object.
"""

import os
import sys

class FakeFieldStorage(dict):
    """
    Fake FieldStorage object.
    """

    def __init__(self, *args, **kwargs):
        """
        Simulates the mod_python FieldStorage object, really just to
        provide the list object.
        
        @return: Pseudo mod_python FieldStorage object
        """

        super(FakeFieldStorage, self).__init__() 
        self.list = self
    
class FakeRequest(object):
    """
    Fake request object
    """

    def __init__(self):
        """
        Simulates the req object common to mod_python development
    
        @return: Pseudo mod_python req object
        """

        environ = os.environ
        self.subprocess_env = environ
        self.content_type = "text/plain"
        self.status = 200
        self.args = environ.get('QUERY_STRING', '')
        self.filename = 'index.py'
        self.hostname = 'localhost'
        self.path_info = environ.get('PATH_INFO', '')
        self.unparsed_uri = '/'
        self.uri = '/'
        self.the_request = 'GET / HTTP/1.1'
        self.connection = FakeRequestConnection()
        self.content_length = -1
        self._headed = 0
        self.headers_out = self
        self.headers = ""
        self.read = sys.stdin.read
        self.server = FakeServer()
        self.headers_in = {'Referer':environ.get('HTTP_REFERER', ''),
                           'Cookie':environ.get('HTTP_COOKIE', '')}
        self.get = FakeFieldStorage()
        self.form = FakeFieldStorage()
       
    def _writeheaders(self):
        self._headed = 1
        sys.stdout.write('status: %s\n' % self.status)
        sys.stdout.write('Content-Type: %s\n' % self.content_type)
        if self.content_length >= 0:
            sys.stdout.write('Content-Length: %s\n' % self.content_length)
        sys.stdout.write(self.headers)
        sys.stdout.write('\n')
        self.write = sys.stdout.write

    def add(self, key, value):
        self.headers += '%s: %s\n' % (key, value)

    def document_root(self):
        return ''

    def get_remote_host(self):
        return None

    def set_content_length(self, len):
        self.content_length = len

    def write(self, s):
        if not self._headed:
            self._writeheaders()
        sys.stdout.write(s)
           
class FakeRequestConnection(object):
    def __init__(self):
        self.local_addr = ['', '']
        
class FakeServer(object):
    def __init__(self):
        self.server_hostname = 'localhost'

# Expose drop in replacements for the real thing
FieldStorage = FakeFieldStorage

