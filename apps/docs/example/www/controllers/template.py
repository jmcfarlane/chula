"""
"""

from example.www.controllers import base

class Template(base.Base):
    def index(self):
        """
        """

        view = self.template('/template.tmpl')
        return view.render(model=self.model)
