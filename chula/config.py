"""
Mange the Chula configuration
"""

from chula.chulaException import *
from chula import collection

class Config(collection.Collection):
    UNSET = 'THIS ATTRIBUTE NEEDS TO BE SET BY YOU'
    supported = ['classpath',
                 'session_db',
                 'session_cache_hosts']

    def __init__(self):
        super(Config, self).__init__()
        self.classpath = self.UNSET
        self.session_db = 'localhost'
        self.session_cache_hosts = ('localhost:11211', 1)

    def __getattr__(self, key):
        if key in self.supported:
            return getattr(self, key, None)
        else:
            raise UnsupportedConfigError(append=key)

    def __setattr__(self, key, value):
        if key in self.supported:
            self.__dict__[key] = value
        else:
            raise UnsupportedConfigError(append=key)
