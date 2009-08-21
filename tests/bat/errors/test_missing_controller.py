from chula import bat

HTML = 'Page not found'

class Test_missing_controller(bat.Bat):
    def test_root(self):
        retval = self.request('/missing_controller')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 404)

    def test_root_with_slash(self):
        retval = self.request('/missing_controller/')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 404)

    def test_method_specified(self):
        retval = self.request('/missing_controller/foobar')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 404)
