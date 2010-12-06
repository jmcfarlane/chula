#! /usr/bin/env python

import os
import sys
from wsgiref.simple_server import make_server

def main():
    # Expose Chula and the "example" python package, as it's not "installed"
    cwd = os.getcwd()
    sys.path.insert(0, cwd + '/../..')
    sys.path.insert(0, cwd)

    from chula.www.adapters.wsgi import adapter
    from model import configuration

    @adapter.wsgi
    def application():
        return configuration.app

    # Setup a simple server using the proxy app and it's configuration
    port = 8080
    httpd = make_server('', port, application)
    try:
        print 'Starting server on: http://localhost:%s' % port
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()
