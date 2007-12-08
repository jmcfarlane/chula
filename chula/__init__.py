"""Chula is a lightweight web framework written in Python

Chula is an MVC style framework that works by routing web requests
thru mod_python to native Python objects (controllers).

Here is the basic flow thru the Chula stack:
    client > apache > mod_python > handler > controller > view > client

Chula has the following dependancies:
    - apache2
    - mod_python
    - postgresql
    - python-2.5
    - simplejson

To use the advanced features of Chula you will also need:
    - memcache

For more information see: http://www.rockfloat.com/projects/chula/
"""

__VERSION__ = '0.0.1'
version = __VERSION__

__all__ = ['collection',
           'config',
           'data',
           'db',
           'ecalendar',
           'error',
           'example',
           'guid',
           'json',
           'memcache',
           'pager',
           'passwd',
           'regex',
           'session',
           'webservice']
