import copy

from chula import config

# Prod config
prod = config.Config()
prod.classpath = 'example.www.controllers'
prod.construction_controller = 'construction'
prod.construction_trigger = '/tmp/chula_example.stop'
prod.debug = False
prod.error_controller = 'error'
prod.session_encryption_key = 'abcd'
prod.local.view_cache = None

# Dev config
dev = copy.deepcopy(prod)
dev.debug = True
