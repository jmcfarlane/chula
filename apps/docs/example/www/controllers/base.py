from mako.template import Template
from mako.lookup import TemplateLookup

import chula
from chula.www import controller

class Base(controller.Controller):
    def __init__(self, env, config):
        """
        Configure default behavior for all controllers
        """

        super(Base, self).__init__(env, config)
        self.model.version = chula.version

    def template(self, view):
        src = self.config.local.root + '/view'
        lookup = TemplateLookup(directories=[src])
        view = Template(filename=src + view, lookup=lookup)

        return view
