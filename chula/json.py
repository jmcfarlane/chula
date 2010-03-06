"""
Wrapper to make it easy to switch from one json library to another
"""

from chula import error

try:
    import simplejson
except:
    try:
        from django.utils import simplejson
    except:
        raise error.MissingDependencyError('Simplejson')

decode = simplejson.loads
encode = simplejson.dumps
