from chula.www import controller

class Sample(controller.Controller):
    def index(self):
        return 'Sample controller'

    def page(self):
        return 'Sample controller:page'
