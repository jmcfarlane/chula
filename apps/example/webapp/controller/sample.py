# Chula imports
from chula import webservice
from chula.www import controller

class Sample(controller.Controller):
    def index(self):
        return 'Sample controller'

    def page(self):
        return 'Sample controller:page'

    @webservice.expose()
    def webservice(self):
        return {'color':'red', 'features':[1, 2, 3, None, 'abc']}
