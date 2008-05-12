"""
The standard Chula URL mapper
"""

from chula.www.mapper import base

class StandardMapper(base.BaseMapper):
    def parse(self):
        parts = self.uri.split('/') 

        # Remove any empty segments
        while '' in parts:
            parts.remove('')
        count = len(parts)

        # Update package, module, method
        if count == 0:
            pass
        elif count == 1:
            self.route.module = parts.pop()
        elif count == 2:
            self.route.method = parts.pop()
            self.route.module = parts.pop()
            self.route.package +=  '.'.join(parts)
        elif count > 2:
            self.route.method = parts.pop()
            self.route.module = parts.pop()
            self.route.package += '.' + '.'.join(parts)
        else:
            raise ValueError('Bad route: %s' % self.route)

        # The class name is always the capitalized module name
        self.route.class_name = self.route.module.capitalize()

        return str(self)
