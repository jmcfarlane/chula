"""
Python classpath based Chula URL mapper
"""

from chula.www.mapper import base

class ClassPathMapper(base.BaseMapper):
    def parse(self):
        # Parse the uri (excluding the querystring)
        parts = self.uri.split('?')[0].split('/')

        # Remove any empty segments
        while '' in parts:
            parts.remove('')
        count = len(parts)

        # Update package, module, method
        if count == 0:
            # Homepage
            pass
        elif count == 1:
            # Root controller using default method
            self.route.method = base.DEFAULT_METHOD
            self.route.module = parts.pop()
        elif count == 2:
            # Root controller using specified method
            self.route.method = parts.pop()
            self.route.module = parts.pop()
            self.route.package += '.'.join(parts)
        elif count > 2:
            # Package controller using specified method
            self.route.method = parts.pop()
            self.route.module = parts.pop()
            self.route.package += '.' + '.'.join(parts)
        else:
            # This can't happen?
            raise ValueError('Bad route: %s' % self.route)

        # The class name is always the capitalized module name
        self.route.class_name = self.route.module.capitalize()

        return str(self)
