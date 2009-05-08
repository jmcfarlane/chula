"""
Chula documentation manual
"""

import os

from docutils import core
from docutils.writers.html4css1 import Writer, HTMLTranslator

from example.www.controllers import base

# Create a writer and reuse where if possible
writer = Writer()

class Manual(base.Base):

    def index(self):
        """
        """
        
        doc = self.env.form_get.get('doc', 'index')
        path = os.path.join(self.config.local.root, 'rst', doc + '.rst')
        self.model.error = False
        self.model.fragment = None

        if os.path.exists(path):
            try:
                rst = open(path).read()
                html = core.publish_parts(rst, writer=writer)
                self.model.fragment = html['html_body']
            except Exception, ex:
                self.model.error = str(ex)

        view = self.template('/manual.tmpl')
        return view.render(model=self.model)

