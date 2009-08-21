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
import datetime
from chula import data
from chula.error import *

class Test_data(unittest.TestCase):
    """A test class for the data module"""
    
    doctest = data
    
    def setUp(self):
        self.int = 7
        self.str = "foobar"
        
    def test_commaify(self):
        self.assertEqual(data.commaify(""), "")
        self.assertEqual(data.commaify(" "), " ")
        self.assertEqual(data.commaify("abcdef"), "abcdef")
        self.assertEqual(data.commaify("1"), "1")
        self.assertEqual(data.commaify("1.20"), "1.20")
        self.assertEqual(data.commaify("10"), "10")
        self.assertEqual(data.commaify("10.1"), "10.10")
        self.assertEqual(data.commaify("10.10"), "10.10")
        self.assertEqual(data.commaify("100"), "100")
        self.assertEqual(data.commaify("100.00"), "100.00")
        self.assertEqual(data.commaify("1000"), "1,000")
        self.assertEqual(data.commaify("1000.45"), "1,000.45")
        self.assertEqual(data.commaify("1000.450"), "1,000.450")
        self.assertEqual(data.commaify("-1000.45"), "-1,000.45")
        self.assertEqual(data.commaify("-10000.45"), "-10,000.45")
        self.assertEqual(data.commaify("-100000.45"), "-100,000.45")
        self.assertEqual(data.commaify("-1000000.45"), "-1,000,000.45")
    
    def test_date_add(self):
        t = datetime.datetime
        self.assertEqual(data.date_add("s", 5,
                         data.str2date("1/1/2005 1:00")),
                         t(2005, 1, 1, 1, 0, 5))
        self.assertEqual(data.date_add("m", 5,
                         data.str2date("1/1/2005 1:00")),
                         t(2005, 1, 1, 1, 5, 0))
        self.assertEqual(data.date_add("s", 5,
                         data.str2date("1/1/2005 1:00:05")),
                         t(2005, 1, 1, 1, 0, 10))

        # A few negative tests:
        self.assertEqual(data.date_add("m", -5,
                         data.str2date("1/1/2005 1:05")),
                         t(2005, 1, 1, 1, 0, 0))
     
    def test_date_diff(self):
        d = datetime.datetime
        # Equal dates
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 27, 22, 15, 00)
        self.assertEqual(data.date_diff(a, b), 0)
        
        # Off by seconds
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 27, 22, 45, 00)
        self.assertEqual(data.date_diff(a, b), 1800)
        
        # Off by 15 seconds which rounds to 0 minutes
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 27, 22, 15, 15)
        self.assertEqual(data.date_diff(a, b, 'm'), 0)
        
        # Off by minutes
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 27, 22, 20, 00)
        self.assertEqual(data.date_diff(a, b, 'm'), 5)
        
        # Off by hours
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 27, 23, 15, 00)
        self.assertEqual(data.date_diff(a, b, 'h'), 1)
        
        # Off by hours (spanning midnight)
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 28, 02, 15, 00)
        self.assertEqual(data.date_diff(a, b, 'h'), 4)
        
        # Off by days
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 28, 22, 15, 00)
        self.assertEqual(data.date_diff(a, b, 'd'), 1)
        
        # Off by negative hours
        a = d(2005, 01, 27, 22, 15, 00)
        b = d(2005, 01, 27, 20, 15, 00)
        self.assertEqual(data.date_diff(a, b, 'h'), -2)
        
        # Off by days involving Feb when NOT a leap year
        a = d(2005, 01, 27, 22, 15, 0)
        b = d(2006, 01, 27, 22, 15, 0)
        self.assertEqual(data.date_diff(a, b, 'd'), 365)
        
        # Off by days involving Feb when IS a leap year
        a = d(2008, 01, 27, 22, 15, 00)
        b = d(2009, 01, 27, 22, 15, 00)
        self.assertEqual(data.date_diff(a, b, 'd'), 366)
    
    def test_date_within_range(self):
        d = datetime.datetime
        fmt = '%H:%M'

        # Now is always 30 minutes from now()
        now = d.now().strftime(fmt)
        self.assertEqual(data.date_within_range(now, 30), True)

        # 20 minutes is within range of 30
        now = d(2005, 10, 4, 21, 35, 45).strftime(fmt)
        then = d(2005, 10, 4, 21, 55, 45)
        self.assertEqual(data.date_within_range(now, 30, then), True)

        # 31 minutes is NOT within range of 30
        now = d(2005, 10, 4, 21, 35, 45).strftime(fmt)
        then = d(2005, 10, 4, 22, 6, 45)
        self.assertEqual(data.date_within_range(now, 30, then), False)

        # Anything in the past cannot be in range
        now = d(2005, 10, 4, 21, 35, 45).strftime(fmt)
        then = d(2005, 10, 4, 21, 34, 45)
        self.assertEqual(data.date_within_range(now, 30, then), False)

    def test_format_phone(self):
        self.assertEqual(data.format_phone("+44-(0)1224-XXXX-XXXX"),
                                           "+44-(0)1224-XXXX-XXXX")
        self.assertEqual(data.format_phone("5551234"), "555-1234")
        self.assertEqual(data.format_phone("555-1234"), "555-1234")
        self.assertEqual(data.format_phone("555-555-1234"), "(555) 555-1234")
        self.assertEqual(data.format_phone("5135551234"), "(513) 555-1234")
        
    def test_format_money(self):
        self.assertEqual(data.format_money(0), "0.00")
        self.assertEqual(data.format_money(.45), "0.45")
        self.assertEqual(data.format_money(-.45), "-0.45")
        self.assertEqual(data.format_money(0.45), "0.45")
        self.assertEqual(data.format_money(10), "10.00")
        self.assertEqual(data.format_money(1000), "1,000.00")
        self.assertEqual(data.format_money(1000000), "1,000,000.00")
        self.assertEqual(data.format_money(1000000.45), "1,000,000.45")
        self.assertEqual(data.format_money(-1000000.45), "-1,000,000.45")
        self.assertEqual(data.format_money(10.000), "10.00")
        self.assertEqual(data.format_money(10.00045), "10.00")
        self.assertRaises(TypeConversionError, data.format_money, 'abc')

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

    def test_isregex(self):
        self.assertEqual(data.isregex(r"abc[a-z]"), True)
        self.assertEqual(data.isregex(r"("), False)

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
        self.assertEqual(data.istag(r'abc'), True)
        self.assertEqual(data.istag(u'abc'), True)

    def test_istags(self):
        self.assertEqual(data.istags("a b"), True)
        self.assertEqual(data.istags(u"a b"), True)
        self.assertEqual(data.istags("a$a b"), False)

    def test_none2empty(self):
        self.assertEqual(data.none2empty(self.int), self.int)
        self.assertEqual(data.none2empty(self.str), self.str)
        self.assertEqual(data.none2empty(""), "")
        self.assertEqual(data.none2empty(None), '')
    
    def test_replace_all(self):
        rall = data.replace_all
        self.assertEqual(rall({'o':'0', 't':'7'},"out"), "0u7")
        self.assertEqual(rall({'aaa':'a', '  b':'b'}, "aaa  b"), "ab")
        self.assertEqual(rall({'aaa':'a', '  b':'b'}, "aaa  b"), "ab")
        self.assertEqual(rall({'a':'A'}, "aaaaaa"), "AAAAAA")
        self.assertRaises(TypeError, rall, {2:5}, "12345")
        self.assertRaises(TypeError, rall, {'a':'A'}, 12345)
        self.assertRaises(TypeError, rall, {'a':'A'}, ['a', 'A'])
    
    def test_str2bool(self):
        self.assertEqual(data.str2bool(True), True)
        self.assertEqual(data.str2bool(False), False)
        self.assertEqual(data.str2bool('true'), True)
        self.assertEqual(data.str2bool('on'), True)
        self.assertEqual(data.str2bool('1'), True)
        self.assertEqual(data.str2bool('y'), True)
        self.assertEqual(data.str2bool(1), True)
        self.assertEqual(data.str2bool('false'), False)
        self.assertEqual(data.str2bool('off'), False)
        self.assertEqual(data.str2bool('0'), False)
        self.assertEqual(data.str2bool('n'), False)
        self.assertEqual(data.str2bool(0), False)
        self.assertRaises(TypeConversionError, data.str2bool, 'abc')
           
    def test_str2date(self):
        d = datetime.datetime
        cv = data.str2date
        self.assertEqual(cv('10/4/2005'), d(2005, 10, 4, 0, 0))
        self.assertEqual(cv('10-4-2005'), d(2005, 10, 4, 0, 0))
        self.assertEqual(cv('10-04-2005'), d(2005, 10, 4, 0, 0))
        self.assertEqual(cv('2005-10-4'), d(2005, 10, 4, 0, 0))
        self.assertEqual(cv('2005-10-04'), d(2005, 10, 4, 0, 0))
        self.assertEqual(cv('10/4/2005 21:35'), d(2005, 10, 4, 21, 35))
        self.assertEqual(cv('10/4/2005 21:35:45'), d(2005, 10, 4, 21, 35, 45))
        self.assertEqual(cv('10/4/2005 21:35:00'), d(2005, 10, 4, 21, 35, 00))
        self.assertEqual(cv('10/4/2005 21:01:00'), d(2005, 10, 4, 21, 01, 00))
        self.assertEqual(cv('2005-10-4 21:01'), d(2005, 10, 4, 21, 01, 00))
        self.assertEqual(cv('2005-10-4 21:01:00.970532-04:00'),
                            d(2005, 10, 4, 21, 01, 00))
        self.assertEqual(cv('2009-04-16 23:16:34.953368+00:00'),
                            d(2009, 4, 16, 23, 16, 34))
        self.assertEqual(cv('2005-10-4 21:01:00-04:00'),
                            d(2005, 10, 4, 21, 01, 00))
        self.assertEqual(cv('2005-10-4 21:01:00+04:00'),
                            d(2005, 10, 4, 21, 01, 00))
        self.assertEqual(cv('2005-10-4 21:01:00'), d(2005, 10, 4, 21, 01, 00))
        self.assertEqual(cv('20051004'), d(2005, 10, 4, 0, 00, 00))
        self.assertEqual(cv('20051004'), d(2005, 10, 4, 0, 00, 00))
        self.assertEqual(cv('10042005'), d(2005, 10, 4, 0, 00, 00))
        self.assertEqual(cv('10.04.2005'), d(2005, 10, 4, 0, 00, 00))
        self.assertEqual(cv('1241579419'), d(2009, 5, 5, 20, 10, 19))
        self.assertEqual(cv('1241579419.'), d(2009, 5, 5, 20, 10, 19))
        self.assertEqual(cv('1241579419.0'), d(2009, 5, 5, 20, 10, 19))
        self.assertEqual(cv('1241579419.00'), d(2009, 5, 5, 20, 10, 19))

        self.assertRaises(TypeConversionError, cv, '2005-10')
        self.assertRaises(TypeConversionError, cv, '2005/21/5')
        self.assertRaises(TypeConversionError, cv, '2005/10/40')
        self.assertRaises(TypeConversionError, cv, '2005/10/21 90:10:00')
        self.assertRaises(TypeConversionError, cv, '2005/10/21 10:75:00')
        self.assertRaises(TypeConversionError, cv, '2005/10/21 10:20:61')
        self.assertRaises(TypeConversionError, cv, '2005/10/21 10:00:00:00')
        self.assertRaises(TypeConversionError, cv, 'abc')
        self.assertRaises(TypeConversionError, cv, '124157941')

    def test_str2tags(self):
        self.assertEqual(data.str2tags(''), [])
        self.assertEqual(data.str2tags('Abc'), ['abc'])
        self.assertEqual(data.str2tags('abc'), ['abc'])
        self.assertEqual(data.str2tags("abc4"), ['abc4'])
        self.assertEqual(data.str2tags('a,b'), ['a','b'])
        self.assertEqual(data.str2tags('a, b'), ['a','b'])
        self.assertEqual(data.str2tags('a,  b'), ['a','b'])
        self.assertEqual(data.str2tags('a,  b,c  d a'), ['a','b','c','d'])
        self.assertEqual(data.str2tags('a b c a'), ['a','b','c'])
        self.assertRaises(TypeConversionError, data.str2tags, 'a;b')
        self.assertRaises(TypeConversionError, data.str2tags, 'a+b')
        self.assertRaises(TypeConversionError, data.str2tags, 'a!b')
        self.assertRaises(TypeConversionError, data.str2tags, "I'd")
        self.assertRaises(TypeConversionError, data.str2tags, 4)
        self.assertRaises(TypeConversionError, data.str2tags, None)
    
    def test_tags2str(self):
        self.assertEqual(data.tags2str(['a']), 'a')
        self.assertEqual(data.tags2str(['a','b']), 'a b')
        self.assertEqual(data.tags2str(['b','a']), 'a b')
        self.assertRaises(ValueError, data.tags2str, '')
        self.assertRaises(ValueError, data.tags2str, None)
        self.assertRaises(ValueError, data.tags2str, 4)
        self.assertRaises(ValueError, data.tags2str, ('a','b'))
        self.assertRaises(TypeConversionError, data.tags2str, ['a','!'])
        self.assertRaises(TypeConversionError, data.tags2str, ['-','*'])
