"""
Chula apache handler
"""

import time

from mod_python import apache as APACHE

import chula
from chula import error
from chula.www import urlmapper

def _handler(req, config):
    if config.add_timer:
        TIME_start = time.time()

    # Fetch the controller via the configured url-mapper
    mapper = urlmapper.UrlMapper(config, req)
    controller = mapper.map()

    # Set the Apache content type (specified by the controller)
    req.content_type = controller.content_type

    # Call the controller method
    html = controller.execute()

    # Persist session and perform garbage collection
    try:
        controller._pre_session_persist()
        controller.session.persist()
    except error.SessionUnableToPersistError():
        # Need to assign an error controller method to call here
        raise
    except Exception:
        # This is a downstream exception, let them handle it
        raise
    finally:
        controller._gc()

    # Write the returned html to the request object.
    # We're manually casting the view as a string because Cheetah
    # templates seem to require it.  If you're not using Cheetah,
    # sorry... str() is cheap  :)
    if not html is None:
        html = str(html)

        # Add info about server info and processing time
        written = False
        if config.add_timer:
            end = html[-8:].strip()
            for node in ('</html>', '</HTML>'):
                if end == node:
                    cost = (time.time() - TIME_start) * 1000
                    try:
                        req.write(html.replace(node, """
                            <div style="display:none;">
                                <div id="CHULA_SERVER">%s</div>
                                <div id="CHULA_COST">%f ms</div>
                            </div>
                            """ % (controller.env['server_hostname'],
                                   cost)))
                        req.write(node)
                        written = True
                    except IOError:
                        if config.debug:
                            raise
                    finally:
                        break

        if not written:
            try:
                req.write(html)
            except IOError:
                if config.debug:
                    raise
    else:
        raise error.ControllerMethodReturnError()


    # If we got here, all is well
    return APACHE.OK

def handler(fcn):
    def wrapper(req):
        config = fcn()
        return _handler(req, config)

    return wrapper

