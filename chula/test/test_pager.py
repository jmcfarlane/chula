import unittest
import doctest
from chula import pager

class Test_pager(unittest.TestCase):
    def makeCallable(self, a, b, c, d):
        page = pager.Pager(a, b, c, d)

    def isWellFormed(self, pager, pagecount):
        selectedcount = 0
        for page in pager:
            # Keep track of selected pages, we test this below...
            if page['selected'] is True:
                selectedcount += 1
            
            # Test that the right keys come back
            if ['selected', 'offset'] != page.keys():
                raise KeyError, page

        # Test that exactly one page is selected
        if selectedcount != 1:
            msg = 'There can only be one selected page, not:%s'
            raise ValueError, msg % selectedcount

        # Test that there are the right number of pages 
        if len(pager) != pagecount:
            msg = 'Invalid number of pages (%s), should have been: %s'

            raise IndexError, msg % (len(pager), pagecount)

        return True

    def test_visiblepages_must_be_odd(self):
        self.assertRaises(ValueError, self.makeCallable, 0, 10, 10, 20)

    def test_offset_cannot_be_less_than_zero(self):
        self.assertRaises(ValueError, self.makeCallable, -1, 10, 10, 20)

    def test_recordcount_is_zero(self):
        p = pager.Pager(0, 0, 5, 5)
        self.assertEquals([], p)

    def test_start_must_be_less_than_recordcount(self):
        self.assertRaises(ValueError, self.makeCallable, 10, 10, 10, 20)

    def test_1st_page_should_be_selected(self):
        p = pager.Pager(0, 50, 5, 5)
        self.assertEquals(True, self.isWellFormed(p, 5))
        self.assertEquals(True, p[0]['selected'])
        self.assertEquals(20, p[-1]['offset'])

    def test_2nd_page_should_be_selected(self):
        p = pager.Pager(6, 50, 5, 5)
        self.assertEquals(True, self.isWellFormed(p, 5))
        self.assertEquals(True, p[1]['selected'])
        self.assertEquals(20, p[-1]['offset'])
    
    def test_middle_page_should_be_selected(self):
        p = pager.Pager(20, 50, 5, 5)
        self.assertEquals(True, self.isWellFormed(p, 5))
        self.assertEquals(True, p[2]['selected'])

    def test_shift_left_by_01_pages(self):
        p = pager.Pager(100, 300, 10, 19)
        self.assertEquals(True, self.isWellFormed(p, 19))
        self.assertEquals(10, p[0]['offset'])
    
    def test_shift_left_by_02_pages(self):
        p = pager.Pager(110, 300, 10, 19)
        self.assertEquals(True, self.isWellFormed(p, 19))
        self.assertEquals(20, p[0]['offset'])

    def test_stop_shifting(self):
        p = pager.Pager(0, 100, 5, 5)
        self.assertEquals(True, self.isWellFormed(p, 5))
        self.assertEquals(0, p[0]['offset'])

        for start in xrange(85, 96, 5):
            p = pager.Pager(start, 100, 5, 5)
            self.assertEquals(True, self.isWellFormed(p, 5))
            self.assertEquals(75, p[0]['offset'])
            self.assertEquals(80, p[1]['offset'])
            self.assertEquals(85, p[2]['offset'])
            self.assertEquals(90, p[3]['offset'])
            self.assertEquals(95, p[4]['offset'])

    def test_total_can_be_less_than_visiblepages(self):
        p = pager.Pager(0, 3, 10, 19)
        self.assertEquals(True, self.isWellFormed(p, 1))
        self.assertEquals(0, p[0]['offset'])

    def test_total_less_than_02_pages(self):
        p = pager.Pager(0, 11, 10, 19)
        self.assertEquals(True, self.isWellFormed(p, 2))
        self.assertEquals(0, p[0]['offset'])
        self.assertEquals(10, p[-1]['offset'])
    
def run_unittest():
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    tests = unittest.makeSuite(Test_pager)
    tests.addTest(doctest.DocTestSuite(pager))
    return tests

if __name__ == '__main__':
    run_unittest()
