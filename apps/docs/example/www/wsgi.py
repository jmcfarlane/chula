"""
Chula example wsgi application
"""

from chula.www.adapters.wsgi import adapter

from example.configuration import prod as config

@adapter.wsgi
def application():
    return config
