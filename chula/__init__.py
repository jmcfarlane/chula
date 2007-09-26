"""
Chula python package
"""

def get_version():
    # TODO: Add checks for git/raw/installed
    return '0.0.0'

__VERSION__ = get_version()

__all__ = ['error',
           'collection',
           'config',
           'data',
           'db',
           'example',
           'guid',
           'json',
           'memcache',
           'pager',
           'passwd',
           'regex',
           'session'
          ]

