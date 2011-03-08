from chula.test import bat

class Test_global_exception(bat.Bat):
    def test_root(self):
        retval = self.request('/global_exception/index')
        self.assertTrue(retval.data.find('Application Error') >= 0)
        self.assertTrue(retval.data.find('variable_not_defined') >= 0)
        self.assertEquals(retval.status, 500)
