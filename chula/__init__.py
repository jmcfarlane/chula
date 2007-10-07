"""
Chula python package
"""

def get_version():
    # TODO: Add checks for git/raw/installed
    return '0.0.0'

__VERSION__ = get_version()
version = __VERSION__

__all__ = ['collection',
           'config',
           'data',
           'db',
           'ecalendar',
           'error',
           'guid',
           'json',
           'memcache',
           'pager',
           'passwd',
           'regex',
           'session',
           'webservice']
