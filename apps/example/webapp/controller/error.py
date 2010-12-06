from chula.www import controller

class Error(controller.Controller):
    def index(self):
        return 'Sorry, the site is down for maintenance'

    def e404(self):
        return 'Page not found'

    def e500(self):
        return 'Trapped Error: %s' % self.model.exception.exception
