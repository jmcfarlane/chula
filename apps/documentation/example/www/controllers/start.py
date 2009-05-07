"""
Getting Started page
"""

from example.www.controllers import base

class Start(base.Base):
    def index(self):
        """
        """

        view = self.template('/start/index.tmpl')
        return view.render(model=self.model)
