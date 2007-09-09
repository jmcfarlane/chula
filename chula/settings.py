"""
Fetch supported user defined settings from ~/settings.py
"""

from chula.chulaException import *

class Settings(object):
    supported = ['session_db',
                 'session_cache_hosts']

    def __init__(self):
        self.session_db = 'localhost'
        self.session_cache_hosts = ('localhost:11211', 1)

    def __getattr__(self, key):
        if key in self.supported:
            return getattr(self, key, None)
        else:
            raise UnsupportedSettingError(append=key)

    def __setattr__(self, key, value):
        if key in self.supported:
            self.__dict__[key] = value
        else:
            raise UnsupportedSettingError(append=key)

    # Also allow dictionary style access
    __getitem__ = __getattr__
    __setitem__ = __setattr__
