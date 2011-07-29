# Chula imports
from chula.www import controller

class Rest(controller.Controller):
    def blog(self):
        return 'blog: %s' % self.env.form_rest

    def user(self):
        return 'user preferences'
