from chula.www import controller

class Test(controller.Controller):
    html = """
    <ol>
        <li><a href="/bad_import/index">bad import</a></li>
        <li><a href="/global_exception/index">global error</a></li>
        <li><a href="/missing/index">missing controller</a></li>
    </ol>
    """

    def index(self):
        return self.html
