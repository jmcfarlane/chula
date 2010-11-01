"""
Wrapper to make it easy to switch from one json library to another
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

# Expose the two methods we care about
decode = json_provider.loads
encode = json_provider.dumps

if __name__ == '__main__':
    data = {'abc':'123', 'foobar':45}
    encoded = encode(data)
    decoded = decode(encoded)
    print('Provider:', json_provider)
    print('Encoded:', encoded)
    print('Decoded:', decoded)
