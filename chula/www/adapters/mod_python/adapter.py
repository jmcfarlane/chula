"""
Chula mod_python adapter
"""

from mod_python import apache as APACHE

from chula.www.adapters import base
from chula.www.adapters.mod_python import env

def _handler(req, config):
    adapter = base.BaseAdapter(config)
    adapter.set_environment(env.Environment(req))

    bfr = []
    for chunk in adapter.execute():
        #req.write(chunk)
        bfr.append(chunk)

    # Set HTTP headers set by the controller
    for header in adapter.env.headers:
        req.headers_out.add(header[0], header[1])

    # Set the content_type and status
    req.content_type = adapter.env.content_type
    req.status = adapter.env.status

    for chunk in bfr:
        req.write(chunk)

    return APACHE.OK

def handler(fcn):
    def wrapper(req):
        config = fcn()
        return _handler(req, config)

    return wrapper
