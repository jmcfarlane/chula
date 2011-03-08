from chula.test import bat

class Test_syntax_exception(bat.Bat):
    def test_root(self):
        retval = self.request('/syntax_exception/index')
        self.assertTrue(retval.data.find('Application Error') >= 0)
        self.assertTrue(retval.data.find('invalid syntax') >= 0)
        self.assertTrue(retval.data.find('syntax_exception.py, line 5') >= 0)
        self.assertEquals(retval.status, 500)
