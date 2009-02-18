"""
Chula mod_python adapter
"""

from mod_python import apache as APACHE

from chula.www.adapters import base
from chula.www.adapters.mod_python import env

def configured_handler(req, config):
    adapter = base.BaseAdapter(config)
    adapter.set_environment(env.Environment(req))

    # Execute the controller and store it's output
    chunks = [c for c in adapter.execute()]

    # Add the headers to the mod_python req object
    for header in adapter.env.headers:
        req.headers_out.add(header[0], header[1])

    # Set the content_type and status
    req.content_type = adapter.env.content_type
    req.status = adapter.env.status

    # Write the data to the client
    try:
        for chunk in chunks:
            req.write(chunk)
    except IOError, ex:
        if config.debug:
            raise

    # All is well
    try:
        return APACHE.OK
    except:
        pass

def handler(fcn):
    def wrapper(req):
        config = fcn()
        return configured_handler(req, config)

    return wrapper
