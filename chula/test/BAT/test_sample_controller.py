from chula import bat

HTML = 'Sample controller'

class Test_sample_controller(bat.Bat):
    def test_root(self):
        retval = self.request('/sample')
        self.assertEquals(retval, HTML)

    def test_with_slash(self):
        retval = self.request('/sample/')
        self.assertEquals(retval, HTML)

    def test_method_specified(self):
        retval = self.request('/sample/page')
        self.assertEquals(retval, HTML + ':page')

    def test_method_specified_with_slash(self):
        retval = self.request('/sample/page/')
        self.assertEquals(retval, HTML + ':page')
