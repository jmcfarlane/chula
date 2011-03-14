"""
Wrapper to make it easy to switch from one json library to another.
Currently this module is searching for a json provider in the
following order:

#. :mod:`json` (builtin)
#. simplejson
#. simpljson (as packaged with Django)

The purpose behind this module is to allow Chula to avoid having a
static copy of a json provider (for older vesions of Python) yet still
*work* in most cases.  If one of the above json providers cannot be
found, a :class:`chula.error.MissingDependencyError` will be raised.
"""

# Python imports
from __future__ import absolute_import

# Chula imports
from chula import error

def _official():
    import json
    return json

def _simplejson():
    import simplejson
    return simplejson

def _django():
    from django.utils import simplejson
    return simplejson

# Fetch the [most] preferred json provider
json_provider = None
for provider in [_official, _simplejson, _django]:
    try:
        json_provider = provider()
        break
    except ImportError:
        pass

# Make sure we found a provider
if json_provider is None:
    msg = 'Simplejson, or Python >=2.6'
    raise error.MissingDependencyError(msg)

# Expose the native methods you'd expect
dumps = json_provider.dumps
loads = json_provider.loads

# Expose legacy methods
decode = json_provider.loads
encode = json_provider.dumps

if __name__ == '__main__':
    data = {'abc':'123', 'foobar':45}
    encoded = encode(data)
    decoded = decode(encoded)
    print('Provider:', json_provider)
    print('Encoded:', encoded)
    print('Decoded:', decoded)
