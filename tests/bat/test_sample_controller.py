from chula.test import bat

HTML = 'Sample controller'

class Test_sample_controller(bat.Bat):
    def test_root(self):
        retval = self.request('/sample')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 200)

    def test_with_slash(self):
        retval = self.request('/sample/')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 200)

    def test_method_specified(self):
        retval = self.request('/sample/page')
        self.assertEquals(retval.data, HTML + ':page')
        self.assertEquals(retval.status, 200)

    def test_method_specified_with_slash(self):
        retval = self.request('/sample/page/')
        self.assertEquals(retval.data, HTML + ':page')
        self.assertEquals(retval.status, 200)
