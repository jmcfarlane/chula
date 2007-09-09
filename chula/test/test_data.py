"""data.py unit tests
"""

#test_data.py - Class to test generic python functions
#
#Copyright (C) 2005 John McFarlane <john.mcfarlane@rockfloat.com>
#
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import unittest
import doctest
import datetime
from chula import data

class Test_data(unittest.TestCase):
    """A test class for the data module"""
    
    def setUp(self):
        self.int = 7
        self.str = "foobar"
        
    def test_chart_scale(self):
        self.assertEqual(data.chart_scale(300), 330.0)
        self.assertEqual(data.chart_scale(150), 170.0)
        self.assertEqual(data.chart_scale(2500), 2750.0)
        self.assertEqual(data.chart_scale(5.5), 10.0)
        self.assertEqual(data.chart_scale('5.5'), 10.0)
        self.assertRaises(ValueError, data.chart_scale, 'abc')
 
    def test_commaify(self):
        #self.assertEqual(data.commaify(""), "") #FIX: handle empty string
        self.assertEqual(data.commaify(" "), " ")
        self.assertEqual(data.commaify("1"), "1")
        self.assertEqual(data.commaify("1000"), "1,000")
        self.assertEqual(data.commaify("1000.45"), "1,000.45")
        self.assertEqual(data.commaify("1000.450"), "1,000.450")
        self.assertEqual(data.commaify("-1000.45"), "-1,000.45")
    
    def test_date_add(self):
        t = datetime.datetime
        self.assertEqual(data.date_add("s", 5, data.str2datetime("1/1/2005 1:00")),
                         t(2005, 1, 1, 1, 0, 5))
        self.assertEqual(data.date_add("m", 5, data.str2datetime("1/1/2005 1:00")),
                         t(2005, 1, 1, 1, 5, 0))
        self.assertEqual(data.date_add("s", 5, data.str2datetime("1/1/2005 1:00:05")),
                         t(2005, 1, 1, 1, 0, 10))
        # A few negative tests:
        self.assertEqual(data.date_add("m", -5, data.str2datetime("1/1/2005 1:05")),
                         t(2005, 1, 1, 1, 0, 0))
     
    def test_datetime_diff(self):
        d = datetime.datetime
        # Equal dates
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 27, 22, 15, 00)
        self.assertEqual(data.datetime_diff(a, b), 0)
        
        # Off by seconds
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 27, 22, 45, 00)
        self.assertEqual(data.datetime_diff(a, b), 1800)
        
        # Off by 15 seconds which rounds to 0 minutes
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 27, 22, 15, 15)
        self.assertEqual(data.datetime_diff(a, b, 'm'), 0)
        
        # Off by minutes
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 27, 22, 20, 00)
        self.assertEqual(data.datetime_diff(a, b, 'm'), 5)
        
        # Off by hours
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 27, 23, 15, 00)
        self.assertEqual(data.datetime_diff(a, b, 'h'), 1)
        
        # Off by hours (spanning midnight)
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 28, 02, 15, 00)
        self.assertEqual(data.datetime_diff(a, b, 'h'), 4)
        
        # Off by days
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 28, 22, 15, 00)
        self.assertEqual(data.datetime_diff(a, b, 'd'), 1)
        
        # Off by negative hours
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 27, 20, 15, 00)
        self.assertEqual(data.datetime_diff(a, b, 'h'), -2)
        
        # Off by days involving Feb when NOT a leap year
        a = d(2005, 01, 27, 22, 15, 0)
        b = d(2006, 01, 27, 22, 15, 0)
        self.assertEqual(data.datetime_diff(a, b, 'd'), 365)
        
        # Off by days involving Feb when IS a leap year
        a = d(2008, 01, 27, 22, 15, 00)
        b = d(2009, 01, 27, 22, 15, 00)
        self.assertEqual(data.datetime_diff(a, b, 'd'), 366)
    
    def test_datetime_within_range(self):
        d = datetime.datetime
        fmt = '%H:%M'
        # Now is always 30 minutes from now()
        str_now = d.now().strftime(fmt)
        self.assertEqual(data.datetime_within_range(str_now, 30), True)
        # 20 minutes is within range of 30
        str_now = d(2005, 10, 4, 21, 35, 45).strftime(fmt)
        self.assertEqual(data.datetime_within_range(str_now, 30, d(2005, 10, 4, 21, 55, 45)), True)
        # 31 minutes is NOT within range of 30
        str_now = d(2005, 10, 4, 21, 35, 45).strftime(fmt)
        self.assertEqual(data.datetime_within_range(str_now, 30, d(2005, 10, 4, 22, 6, 45)), False)
        # Anything in the past cannot be in range
        str_now = d(2005, 10, 4, 21, 35, 45).strftime(fmt)
        self.assertEqual(data.datetime_within_range(str_now, 30, d(2005, 10, 4, 21, 34, 45)), False)

    def test_fmt_phone(self):
        self.assertEqual(data.fmt_phone("+44-(0)1224-XXXX-XXXX"), "+44-(0)1224-XXXX-XXXX")
        self.assertEqual(data.fmt_phone("5551234"), "555.1234")
        self.assertEqual(data.fmt_phone("555-1234"), "555-1234")
        self.assertEqual(data.fmt_phone("555-555-1234"), "(555) 555.1234")
        self.assertEqual(data.fmt_phone("5135551234"), "(513) 555.1234")
        
    def test_fmt_money(self):
        self.assertEqual(data.fmt_money(0), "0.00")
        self.assertEqual(data.fmt_money(.45), "0.45")
        self.assertEqual(data.fmt_money(-.45), "-0.45")
        self.assertEqual(data.fmt_money(0.45), "0.45")
        self.assertEqual(data.fmt_money(10), "10.00")
        self.assertEqual(data.fmt_money(1000), "1,000.00")
        self.assertEqual(data.fmt_money(1000000), "1,000,000.00")
        self.assertEqual(data.fmt_money(1000000.45), "1,000,000.45")
        self.assertEqual(data.fmt_money(-1000000.45), "-1,000,000.45")
    
    # TODO: remove in 0.0.2
#    def test_isarray(self):
#        self.assertEqual(data.isarray(()), True) # Empty tuple
#        self.assertEqual(data.isarray(('a',)), True) # Single element tuple
#        self.assertEqual(data.isarray(('a', 'b')), True)
#        self.assertEqual(data.isarray(['a']), True)
#        self.assertEqual(data.isarray({'a':'a'}), True)
#        self.assertEqual(data.isarray('a'), False)
    
    def test_isdate(self):
        self.assertEqual(data.isdate('1/1/2005'), True)
        self.assertEqual(data.isdate('1-1-2005'), True)
        self.assertEqual(data.isdate('2005-01-01'), True)
        self.assertEqual(data.isdate('1/1/2005 10:45'), True)
        self.assertEqual(data.isdate('1/1/2005 10:45:00'), True)
        self.assertEqual(data.isdate('1/1/20050'), False)
        self.assertEqual(data.isdate(None), False)
        self.assertEqual(data.isdate('a'), False)
        self.assertEqual(data.isdate(1), False)
        self.assertEqual(data.isdate(''), False)
        self.assertEqual(data.isdate("'"), False)

    def test_isboolean(self):
        self.assertEqual(data.isboolean(True), True)
        self.assertEqual(data.isboolean('true'), False)
        self.assertEqual(data.isboolean('true', bool_strict=False), True)
        self.assertEqual(data.isboolean(1, bool_strict=False), True)
        self.assertEqual(data.isboolean('on', bool_strict=False), True)
        self.assertEqual(data.isboolean('True', bool_strict=False), True)
        self.assertEqual(data.isboolean('TRUE', bool_strict=False), True)
           
    def test_isdict(self):
        self.assertEqual(data.isdict(()), False) # Empty tuple
        self.assertEqual(data.isdict(('a',)), False) # Single element tuple
        self.assertEqual(data.isdict(('a', 'b')), False)
        self.assertEqual(data.isdict(['a']), False)
        self.assertEqual(data.isdict({'a':'a'}), True)
        self.assertEqual(data.isdict('a'), False)
    
    def test_isint(self):
        self.assertEqual(data.isint(0), True)
        self.assertEqual(data.isint(00), True)
        self.assertEqual(data.isint(12), True)
        self.assertEqual(data.isint(-1), True)
        self.assertEqual(data.isint('1'), False)
        self.assertEqual(data.isint('1', bool_strict=False), True)
        self.assertEqual(data.isint(None), False)
        self.assertEqual(data.isint([]), False)
    
    def test_islist(self):
        self.assertEqual(data.islist(()), False) # Empty tuple
        self.assertEqual(data.islist(('a',)), False) # Single element tuple
        self.assertEqual(data.islist(('a', 'b')), False)
        self.assertEqual(data.islist(['a']), True)
        self.assertEqual(data.islist({'a':'a'}), False)
        self.assertEqual(data.islist('a'), False)
 
    def test_isstr(self):
        self.assertEqual(data.isstr(self.int), False)
        self.assertEqual(data.isstr(self.str), True)
        self.assertEqual(data.isstr(''), True)
        self.assertEqual(data.isstr(None), False)
        self.assertEqual(data.isstr(' '), True)
        self.assertEqual(data.isstr(True), False)
        self.assertEqual(data.isstr(True, bool_strict=False), True)
        self.assertEqual(data.isstr('45', bool_strict=False), True)
        
        class Foo(object):
            def __str__(self):
                raise Exception('str() not supported')
        obj_no_str = Foo()
        
        self.assertEqual(data.isstr(obj_no_str, bool_strict=False), False)

    def test_istag(self):
        self.assertEqual(data.istag("'"), False)
        self.assertEqual(data.istag("''"), False)
        self.assertEqual(data.istag('"'), False)
        self.assertEqual(data.istag('""'), False)
        self.assertEqual(data.istag(''), False)
        self.assertEqual(data.istag(' '), False)
        self.assertEqual(data.istag('  '), False)
        self.assertEqual(data.istag(None), False)
        self.assertEqual(data.istag('abc'), True)
        self.assertEqual(data.istag('a'), True)
        self.assertEqual(data.istag('B'), True)
        self.assertEqual(data.istag('4'), True)
        self.assertEqual(data.istag(4), False)
        self.assertEqual(data.istag('a,b'), False)

    def test_istuple(self):
        self.assertEqual(data.istuple(()), True) # Empty tuple
        self.assertEqual(data.istuple(('a',)), True) # Single element tuple
        self.assertEqual(data.istuple(('a', 'b')), True)
        self.assertEqual(data.istuple(['a']), False)
        self.assertEqual(data.istuple({'a':'a'}), False)
        self.assertEqual(data.istuple('a'), False)
    
    def test_none2empty(self):
        self.assertEqual(data.none2empty(self.int), self.int)
        self.assertEqual(data.none2empty(self.str), self.str)
        self.assertEqual(data.none2empty(""), "")
        self.assertEqual(data.none2empty(None), '')
    
    def test_replace_all(self):
        self.assertEqual(data.replace_all({'o':'0', 't':'7'}, "out"), "0u7")
        self.assertEqual(data.replace_all({'aaa':'a', '  b':'b'}, "aaa  b"), "ab")
        self.assertEqual(data.replace_all({'aaa':'a', '  b':'b'}, "aaa  b"), "ab")
        self.assertEqual(data.replace_all({'a':'A'}, "aaaaaa"), "AAAAAA")
        self.assertRaises(TypeError, data.replace_all, {2:5}, "12345")
        self.assertRaises(TypeError, data.replace_all, {'a':'A'}, 12345)
        self.assertRaises(TypeError, data.replace_all, {'a':'A'}, ['a', 'A'])
    
    def test_str2datetime(self):
        d = datetime.datetime
        self.assertEqual(data.str2datetime("10/4/2005"), d(2005, 10, 4, 0, 0))
        self.assertEqual(data.str2datetime("10-4-2005"), d(2005, 10, 4, 0, 0))
        self.assertEqual(data.str2datetime("2005-10-4"), d(2005, 10, 4, 0, 0))
        self.assertEqual(data.str2datetime("2005-10-04"), d(2005, 10, 4, 0, 0))
        self.assertEqual(data.str2datetime("10/4/2005 21:35"), d(2005, 10, 4, 21, 35))
        self.assertEqual(data.str2datetime("10/4/2005 21:35:45"), d(2005, 10, 4, 21, 35, 45))
        self.assertEqual(data.str2datetime("10/4/2005 21:35:00"), d(2005, 10, 4, 21, 35, 00))
        self.assertEqual(data.str2datetime("10/4/2005 21:01:00"), d(2005, 10, 4, 21, 01, 00))
        self.assertEqual(data.str2datetime("20051004"), d(2005, 10, 4, 0, 00, 00))
        self.assertEqual(data.str2datetime("20051004"), d(2005, 10, 4, 0, 00, 00))
        self.assertRaises(ValueError, data.str2datetime, 'abc')

    def test_str2tags(self):
        self.assertEqual(data.str2tags(''), [])
        self.assertEqual(data.str2tags('Abc'), ['abc'])
        self.assertEqual(data.str2tags('abc'), ['abc'])
        self.assertEqual(data.str2tags("abc4"), ['abc4'])
        self.assertEqual(data.str2tags('a,b'), ['a','b'])
        self.assertEqual(data.str2tags('a, b'), ['a','b'])
        self.assertEqual(data.str2tags('a+b'), ['a','b'])
        self.assertEqual(data.str2tags('a,  b'), ['a','b'])
        self.assertEqual(data.str2tags('a,  b,c  d a'), ['a','b','c','d'])
        self.assertEqual(data.str2tags('a b c a'), ['a','b','c'])
        self.assertRaises(ValueError, data.str2tags, 'a;b')
        self.assertRaises(ValueError, data.str2tags, 'a!b')
        self.assertRaises(ValueError, data.str2tags, "I'd")
        self.assertRaises(ValueError, data.str2tags, 4)
        self.assertRaises(ValueError, data.str2tags, None)
    
    def test_tags2str(self):
        self.assertEqual(data.tags2str(['a']), 'a')
        self.assertEqual(data.tags2str(['a','b']), 'a b')
        self.assertEqual(data.tags2str(['b','a']), 'a b')
        self.assertRaises(ValueError, data.tags2str, '')
        self.assertRaises(ValueError, data.tags2str, None)
        self.assertRaises(ValueError, data.tags2str, 4)
        self.assertRaises(ValueError, data.tags2str, ('a','b'))
        self.assertRaises(ValueError, data.tags2str, ['a','!'])
        self.assertRaises(ValueError, data.tags2str, ['-','*'])
    
    def test_uid(self):
        self.assertEqual(len(data.uid(35)), 35)
        self.assertEqual(len(data.uid(15)), 15)
        self.assertRaises(Exception, data.uid, 14)
    
def run_unittest():
    # Never change this, leave as is
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    # Replace "example" with the name of your test class and module name
    tests = unittest.makeSuite(Test_data)
    tests.addTest(doctest.DocTestSuite(data))
    return tests

if __name__ == '__main__':
    # Never change this, leave as is
    run_unittest()
