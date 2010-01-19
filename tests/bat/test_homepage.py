from chula.test import bat

HTML = 'Hello <a href="home/foo">world</a>'

class Test_homepage(bat.Bat):
    def test_root(self):
        retval = self.request('')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 200)

    def test_with_slash(self):
        retval = self.request('/')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 200)

    def test_controller_specified(self):
        retval = self.request('/home')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 200)

    def test_controller_specified_with_slash(self):
        retval = self.request('/home/')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 200)

    def test_controller_fq_specified(self):
        retval = self.request('/home/index')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 200)

    def test_controller_fq_specified_with_slash(self):
        retval = self.request('/home/index/')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 200)
