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
    p.add_option('-c', '--config',
                 dest='config_module',
                 help='Module name containing app configuration')
    p.add_option('-o', '--config-object',
                 dest='config_obj',
                 help='Configuration object inside the config')
    p.add_option('-p', '--port',
                 help='TCP port to run the webserver on')
    p.add_option('-t', '--timeout',
                 help='Max time in sec per request if provider supported')
    p.add_option('-w', '--workers',
                 help='Number of workers if the provider supports it')
    p.add_option('-P', '--provider',
                 help='Use the specified provider (gevent, gunicorn, etc)')

    # Defaults
    p.set_defaults(config_module='configuration')
    p.set_defaults(config_obj='app')
    p.set_defaults(debug=False)
    p.set_defaults(port=8080)
    p.set_defaults(timeout=120)
    p.set_defaults(workers=4)

    return (p, p.parse_args())

def _builtin(application, options):
    from wsgiref.simple_server import make_server
    httpd = make_server('', int(options.port), application)
    print 'WSGI provider: wsgiref.simple_server (builtin)'
    return httpd

def _gevent(application, options):
    from gevent import wsgi
    httpd = wsgi.WSGIServer(('', int(options.port)), application)
    print 'WSGI provider: gevent.wsgi'
    return httpd

def _gunicorn(application, options):
    from gunicorn.app import base
    class Gunicorn(base.Application):
        sys.argv = [] # Stop gunicorn from choking on our optparse options
        def init(self, parser, opts, args):
            return {'bind': '0.0.0.0:%s' % options.port,
                    'timeout': int(options.timeout),
                    'workers': options.workers}

        def load(self):
            return application

    httpd = Gunicorn()
    print 'WSGI provider: gunicorn.app.base.Application'
    return httpd

def _tornado(application, options):
    from tornado import httpserver, ioloop, wsgi
    container = wsgi.WSGIContainer(application)
    httpd = httpserver.HTTPServer(container)
    httpd.listen(int(options.port))
    print 'WSGI provider: tornado.httpserver.HTTPServer'
    return ioloop.IOLoop.instance()

def wsgi_provider(application, options):
    if options.provider:
        providers = [getattr(sys.modules[__name__], '_%s' % options.provider)]
    else:
        providers = [_gevent, _gunicorn, _tornado, _builtin]

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

        for method in ['run', 'serve_forever', 'start']:
            if hasattr(httpd, method):
                getattr(httpd, method)()
        else:
            print 'Chula does not know how to use this wsgi provider'
            print 'Type of provider given:', httpd
            sys.exit(1)

    except KeyboardInterrupt:
        sys.exit()

