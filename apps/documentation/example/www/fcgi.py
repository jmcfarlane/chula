"""
Chula example fastcgi application
"""

from chula.www.adapters.fcgi import adapter

from example.configuration import prod as config

@adapter.fcgi
def application():
    return config
