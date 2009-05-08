"""
Chula sample fastcgi server
"""

import os
import sys

try:
    from flup.server.fcgi import WSGIServer
except ImportError:
    from chula.www.fcgi import WSGIServer
    print "Unable to import flup.server.fcgi import WSGIServer"
    print " >>> Falling back on old version available in Chula"

# Expose the "example" python package, as it's not "installed"
cwd = os.getcwd()
sys.path.insert(0, cwd)

from example.configuration import prod as config
from example.www.fcgi import application

# Start the server which will handle calls from the webserver
sock = os.environ.get('FCGI_SOCK', '/tmp/chula_example_fcgi.sock')
print 'Opening FastCGI socket:', sock
WSGIServer(application, bindAddress=sock).run()
