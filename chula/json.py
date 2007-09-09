"""
Wrapper to make it easy to switch from one json library to another
"""

USE='simplejson'

if USE == 'simplejson':
    import simplejson
    decode = simplejson.loads
    encode = simplejson.dumps

elif USE == 'cjson':
    assert 'cjson is not supported just yet'
