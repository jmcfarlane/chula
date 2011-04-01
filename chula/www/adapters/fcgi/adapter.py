"""
Chula fastcgi adapter
"""

# Python imports
from httplib import responses

# Project imports
from chula.www.adapters import base
from chula.www.adapters.fcgi import env

def configured_app(environ, start_response, config):
    adapter = base.BaseAdapter(config)
    adapter.set_environment(env.Environment(environ))

    # Execute the controller and store it's output
    chunks = [c for c in adapter.execute()]

    # Add the content type to the headers
    adapter.add_header(('Content-Type', adapter.env.content_type))

    # Execute the wsgi callback
    status = '%s %s' % (adapter.env.status, responses[adapter.env.status])
    start_response(status, adapter.env.headers)

    # Yield the data to the client
    for chunk in chunks:
        yield chunk

    # Clean house
    adapter._gc()

def fcgi(fcn):
    def wrapper(environ, start_response):
        config = fcn()
        return configured_app(environ, start_response, config)

    return wrapper
