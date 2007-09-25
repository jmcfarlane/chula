"""
Chula python package
"""

def get_version():
    # TODO: Add checks for git/raw/installed
    return '0.0.0'

__VERSION__ = get_version()

__all__ = ['chulaException.py',
           'collection.py',
           'config.py',
           'data.py',
           'db.py',
           'example.py',
           'guid.py',
           'json.py',
           'memcache.py',
           'pager.py',
           'passwd.py',
           'regex.py',
           'session.py'
          ]

