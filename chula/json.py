"""
Wrapper to make it easy to switch from one json library to another
"""

from chula import error


USE='simplejson'

if USE == 'simplejson':
    try:
        import simplejson
    except:
        raise error.MissingDependencyError('Simplejson')
    decode = simplejson.loads
    encode = simplejson.dumps

elif USE == 'cjson':
    assert 'cjson is not supported just yet'
