"""
Python route/route based Chula URL mapper
"""

import re

from chula.www.mapper import base

class RegexMapper(base.BaseMapper):
    def __init__(self, config, env, routes):
        super(RegexMapper, self).__init__(config, env)
        self.routes = routes

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

        #print 'set route:', self.route
        return self.route
        
    def parse(self):
        # Set the default route
        #self._process_route(self.routes[0], force=True)

        # Process each route looking for a match
        for route in self.routes:
            if not self._process_route(route) is None:
                break

        return str(self)
