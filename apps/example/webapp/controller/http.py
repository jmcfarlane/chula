from chula.www import controller

class Http(controller.Controller):
    def _format(self, d):
        return '\n'.join('%s==%s' % (k,v) for k,v in d.items())

    def render_form(self):
        return self._format(self.env.form)

    def render_form_get(self):
        return self._format(self.env.form_get)

    def render_form_post(self):
        return self._format(self.env.form_post)
