"""
Python route/route based Chula URL mapper
"""

import re

from chula import logger
from chula.www.mapper import base

class RegexMapper(base.BaseMapper):
    def __init__(self, config, env, route_map):
        super(RegexMapper, self).__init__(config, env)
        self.route_map = route_map
        self.log = logger.Logger(config).logger('chula.www.mapper.regex')

    def _process_route(self, route, force=False):
        regex, target = route
        if re.match(regex, self.uri) is None and force is False:
            return

        # Pull off the method() and module
        parts = target.split('.')
        self.route.method = parts.pop()
        self.route.module = parts.pop()

        # Pull off the package (if specified)
        if parts:
            self.route.package += '.' + '.'.join(parts)

        self.log.debug('Set route: %s via %s' % (self.route, regex))
        return self.route
        
    def parse(self):
        # Process each route looking for a match
        for route in self.route_map:
            if not self._process_route(route) is None:
                break

        # The class name is always the capitalized module name
        self.route.class_name = self.route.module.capitalize()

        return str(self)
