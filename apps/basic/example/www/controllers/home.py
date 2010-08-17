from chula.www import controller

class Home(controller.Controller):
    def index(self):
        return 'Hello <a href="home/foo">world</a>'

    def foo(self):
        return 'This is the method "foo" of the home controller'

    def raw(self):
        return self.env.form_raw
