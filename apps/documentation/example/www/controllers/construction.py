"""
Under construction page
"""

from example.www.controllers import base

class Construction(base.Base):
    def index(self):
        self.model.msg = 'Sorry, the site is down for maintenance'
        
        view = self.template('/construction.tmpl')
        return view.render(model=self.model)
