"""
Manage the environment when python is using fcgi
"""

import os
import socket

from chula.www.adapters.wsgi import env

FCGI = 'FCGI/WSGI'
PATH = os.environ.get('PATH')

class Environment(env.Environment):
    def __init__(self, environ):
        super(Environment, self).__init__(environ)
        
        # Indicate what type of adapter this is
        self.chula_adapter = FCGI

        # Set the remote_host from the remote_addr
        self.REMOTE_HOST = socket.getfqdn(self.REMOTE_ADDR)

        # Set the path
        self.PATH = PATH
