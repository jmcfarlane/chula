from chula.www import controller

class Test(controller.Controller):
    html = """
    <ol>
        <li><a href="/imports/bad_import/index">bad import</a></li>
        <li><a href="/imports/global_exception/index">global error</a></li>
        <li><a href="/imports/missing/index">missing controller</a></li>
    </ol>
    """

    def index(self):
        return self.html
