from chula import bat

HTML = 'Hello <a href="home/foo">world</a>'

class Test_homepage(bat.Bat):
    def test_root(self):
        retval = self.request('')
        self.assertEquals(retval, HTML)

    def test_with_slash(self):
        retval = self.request('/')
        self.assertEquals(retval, HTML)

    def test_controller_specified(self):
        retval = self.request('/home')
        self.assertEquals(retval, HTML)

    def test_controller_specified_with_slash(self):
        retval = self.request('/home')
        self.assertEquals(retval, HTML)
