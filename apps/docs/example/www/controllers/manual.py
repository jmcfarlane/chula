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
    def _code(self, path):
        """
        """
        
        path = os.path.join(self.config.local.root, path)
        self.model.code_path = path

        try:
            self.model.fragment = open(path).read()
        except Exception, ex:
            self.model.error = str(ex)

        view = self.template('/code.tmpl')
        return view.render(model=self.model)

    def _rst(self, path):
        """
        """
        
        path = os.path.join(self.config.local.root, 'rst', path + '.rst')

        if os.path.exists(path):
            try:
                rst = open(path).read()
                html = core.publish_parts(rst, writer=writer)
                self.model.fragment = html['html_body']
            except Exception, ex:
                self.model.error = str(ex)

        view = self.template('/manual.tmpl')
        return view.render(model=self.model)

    def index(self):
        """
        """

        self.model.error = False
        self.model.fragment = None
        
        if 'doc' in self.env.form_get:
            doc = self.env.form_get.get('doc', 'index')
            return self._rst(doc)
        elif 'code' in self.env.form_get:
            code = self.env.form_get.get('code', 'index')
            return self._code(code)
