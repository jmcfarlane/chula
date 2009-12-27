import os

from chula import config

# Development configuration
dev = config.Config()
dev.classpath = 'example.www.controllers'
dev.construction_controller = 'error'
dev.construction_trigger = '/tmp/chula_example.stop'
dev.debug = True
dev.error_controller = 'error'
dev.session = False

dev.mapper = (
    (r'^$', 'home.index'),
    (r'^/\?foo=bar$', 'home.foo'),
)
