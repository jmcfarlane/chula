from chula import webservice
from chula.www.controller import base

class Webservice(base.Controller):
    @webservice.expose(transport='ASCII')
    def ascii(self):
        return {'some':'payload'}

    @webservice.expose()
    def broken(self):
        return 0 / 0

    @webservice.expose(transport='PICKLE')
    def pickle(self):
        return {'some':'payload'}

    @webservice.expose()
    def simple_json(self):
        return {'some':'payload'}

    @webservice.expose(x_header=True)
    def xjson(self):
        return {'some':'payload'}

