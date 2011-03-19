# Python imports
from wsgiref.simple_server import make_server
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
                 dest='port',
                 help='TCP port to run the webserver on')
    # Defaults
    p.set_defaults(config_module='configuration')
    p.set_defaults(config_obj='app')
    p.set_defaults(debug=False)
    p.set_defaults(port=8080)

    return (p, p.parse_args())

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

    # Setup a simple server using the proxy app and it's configuration
    port = int(options.port)
    httpd = make_server('', port, application)
    try:
        print 'Starting server on: http://localhost:%s' % port
        if 'log' in app_config:
            print 'Errors log:', app_config.log
            if app_config.debug:
                print 'Debug log: ', app_config.log + '.debug'

        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit()

