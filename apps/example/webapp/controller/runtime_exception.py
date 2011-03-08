from chula.www import controller

class Runtime_exception(controller.Controller):
    def index(self):
        return str(0 / 0)
