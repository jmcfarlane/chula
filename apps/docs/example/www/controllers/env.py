"""
Environment controller
"""

from example.www.controllers import base

class Env(base.Base):
    def index(self):
        """
        Homepage
        """

        view = self.template('/env.tmpl')
        return view.render(model=self.model)
