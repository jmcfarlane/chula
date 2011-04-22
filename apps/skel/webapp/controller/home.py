from controller import base

class Home(base.Controller):
    def index(self):
        return self.render('Hello world')

    def foo(self):
        return self.render('Foo')
