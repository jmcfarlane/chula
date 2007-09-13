"""
Mange the Chula configuration
"""

from chula.chulaException import *
from chula import collection

class Config(collection.Collection):
    UNSET = 'THIS ATTRIBUTE NEEDS TO BE SET BY YOU'
    supported = ['classpath',
                 'session_db',
                 'session_host',
                 'session_port',
                 'session_memcache']

    def __init__(self):
        self.classpath = self.UNSET
        self.session_db = 'chula_session'
        self.session_host = 'localhost'
        self.session_port = 5432
        self.session_memcache = [('localhost:11211', 1)]

    def __getitem__(self, key):
        if key in self.supported:
            return self.get(key)
        else:
            raise UnsupportedConfigError(append=key)

    def __setitem__(self, key, value):
        if key in self.supported:
            self.__dict__[key] = value
        else:
            raise UnsupportedConfigError(append=key)
