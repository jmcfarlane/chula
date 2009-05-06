"""
Home controller for the application, handles requests to: /
"""

from example.www.controllers import base

class Home(base.Base):
    def index(self):
        """
        Homepage
        """

        view = self.template('/home.tmpl')
        return view.render(model=self.model)
