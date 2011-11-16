# Python imports
import imp
import optparse
import os
import sys

# Project imports
from chula.www.adapters.wsgi import adapter

def usage():
    return """Usage: %prog [options] path/to/app

Help:

    This script relies upon a somewhat consistent application
    structure.  The typical structure of an app would look something
    like:

    user# tree -d apps/example/webapp
    apps/example/webapp/
    |-- controller
    |-- model
    |-- view
    `-- www

    Typically "controller" and "model" are python packages, though
    their names can be different, it's really up to you.  This script
    does make an assumption though that the configuration and
    controllers can be found in the first level of directories (say
    configuration.py in model, and home.py in controller).

    Examples:

    # If you have configuration.py and an "app" variable inside it:
    %prog /path/to/app

    # For an app with config.py and a "prod" variable inside it:
    %prog -c config -o prod /path/to/app
"""

def getopts():
    p = optparse.OptionParser(usage())
    p.add_option('-a', '--access-log',
                 dest='access_log',
                 help='Access log to write to, "-" for stdout')
    p.add_option('-c', '--config',
                 dest='config_module',
                 help='Module name containing app configuration')
    p.add_option('-k', '--keep-alive',
                 dest='keep_alive',
                 help='Keep-Alive in seconds if supported by provider')
    p.add_option('-l', '--preload',
                 action='store_true',
                 help='Preload prior to forking if supported by provider')
    p.add_option('-m', '--max-requests',
                 dest='max_requests',
                 help='Max requests per worker before re-spawning')
    p.add_option('-o', '--config-object',
                 dest='config_obj',
                 help='Configuration object inside the config')
    p.add_option('-p', '--port',
                 help='TCP port to run the webserver on')
    p.add_option('-t', '--timeout',
                 help='Max time in sec per request if provider supported')
    p.add_option('-w', '--workers',
                 help='Number of workers if the provider supports it')
    p.add_option('-W', '--worker-provider',
                 dest='worker_provider',
                 help='Type of worker class to use if supported by provider')
    p.add_option('-P', '--provider',
                 help='Use the specified provider (gevent, gunicorn, etc)')

    # Defaults
    p.set_defaults(access_log='-')
    p.set_defaults(config_module='configuration')
    p.set_defaults(config_obj='app')
    p.set_defaults(debug=False)
    p.set_defaults(keep_alive=2)
    p.set_defaults(max_requests=0)
    p.set_defaults(port=8080)
    p.set_defaults(preload=False)
    p.set_defaults(timeout=120)
    p.set_defaults(worker_provider='sync')
    p.set_defaults(workers=4)

    return (p, p.parse_args())

def _builtin(application, options):
    print 'WSGI provider: wsgiref.simple_server (builtin)'
    from wsgiref.simple_server import make_server
    httpd = make_server('', int(options.port), application)
    return httpd

def _eventlet(application, options):
    print 'WSGI provider: eventlet.wsgi'
    import eventlet
    from eventlet import wsgi
    e = eventlet.listen(('', int(options.port)))
    return lambda : wsgi.server(e, application)

def _gevent(application, options):
    print 'WSGI provider: gevent.wsgi'
    from gevent import wsgi
    httpd = wsgi.WSGIServer(('', int(options.port)), application)
    return httpd

def _gunicorn(application, options):
    print 'WSGI provider: gunicorn.app.base.Application'
    from gunicorn.app import base
    from gunicorn import config
    class Gunicorn(base.Application):
        sys.argv = [] # Stop gunicorn from choking on our optparse options
        def init(self, parser, opts, args):
            c = {'bind': '0.0.0.0:%s' % options.port,
                 'max_requests': int(options.max_requests),
                 'preload_app': options.preload,
                 'keepalive': int(options.keep_alive),
                 'timeout': int(options.timeout),
                 'worker_class': options.worker_provider,
                 'workers': options.workers}
            if hasattr(config, 'AccessLog'):
                c.update({'accesslog':options.access_log})
            return c

        def load(self):
            return application

    httpd = Gunicorn()
    return httpd

def _tornado(application, options):
    print 'WSGI provider: tornado.httpserver.HTTPServer'
    from tornado import httpserver, ioloop, wsgi
    container = wsgi.WSGIContainer(application)
    httpd = httpserver.HTTPServer(container)
    httpd.listen(int(options.port))
    return ioloop.IOLoop.instance()

def wsgi_provider(application, options):
    if options.provider:
        providers = [getattr(sys.modules[__name__], '_%s' % options.provider)]
    else:
        providers = [_gevent, _gunicorn, _eventlet, _tornado, _builtin]

    for provider in providers:
        try:
            return provider(application, options)
        except (ImportError, NameError):
            pass

    raise Exception('Unable to find a wsgi provider')

def run():
    # Parse command line options
    parser, (options, args) = getopts()

    if not args:
        print 'Error: Please specify the path to your app'
        parser.print_help()
        sys.exit(1)

    options.app = args.pop(0)
    if not os.path.exists(options.app):
        print 'Error: Specified path does not exist:', options.app
        parser.print_help()
        sys.exit(1)

    # Expose the application's top level package(s)
    app_root = os.path.expanduser(options.app)
    sys.path.append(app_root)
    for d in os.listdir(app_root):
        sys.path.append(os.path.join(options.app, d))
    fp, pathname, description = imp.find_module(options.config_module)
    app_config_module = imp.load_module('app', fp, pathname, description)

    try:
        app_config = getattr(app_config_module, options.config_obj)
    except AttributeError, ex:
        print 'Error: Unable to find your application, sorry :/'
        print 'CONFIG_MODULE searched for: %s' % options.config_module
        print 'CONFIG_OBJ searched for: %s' % options.config_obj
        parser.print_help()
        sys.exit(1)

    @adapter.wsgi
    def application():
        return app_config

    httpd = wsgi_provider(application, options)

    try:
        print 'Starting server on: http://localhost:%s' % options.port
        if 'log' in app_config:
            print 'Errors log:', app_config.log
            if app_config.debug:
                print 'Debug log: ', app_config.log + '.debug'

        for attribute in ['run', 'serve_forever', 'start', None]:
            if attribute and hasattr(httpd, attribute):
                httpd = getattr(httpd, attribute)()
                break

        if callable(httpd):
            httpd()
        else:
            print 'Chula does not know how to use this wsgi provider'
            print 'Type of provider given:', httpd
            sys.exit(1)

    except KeyboardInterrupt:
        sys.exit()

