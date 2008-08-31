"""
Chula wsgi adapter
"""

from chula.www.adapters import base
from chula.www.adapters.wsgi import env

def _application(environ, start_response, config):
    adapter = base.BaseAdapter(config)
    adapter.set_environment(env.Environment(environ))
    adapter.set_cookies(environ.get('HTTP_COOKIE', {}))

    bfr = []
    for chunk in adapter.execute():
        #yield chunk
        bfr.append(chunk)

    adapter.close()
    headers = adapter.set_headers([('Content-Type', adapter.env.content_type)])
    
    start_response('%s OK' % adapter.env.status, headers) 

    return ''.join(bfr)

def wsgi(fcn):
    def wrapper(environ, start_response):
        config = fcn()
        return _application(environ, start_response, config)

    return wrapper
