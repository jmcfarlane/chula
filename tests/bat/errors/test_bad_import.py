from chula import bat

class Test_bad_import(bat.Bat):
    def test_root(self):
        retval = self.request('/imports/bad_import/index')
        self.assertTrue(retval.data.find('Trapped Error') >= 0)
        self.assertTrue(retval.data.find('intentionally') >= 0, retval.data)
        self.assertEquals(retval.status, 500)