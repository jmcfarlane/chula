"""
db.py unit tests
"""

#test_db.py - Class to test generic python functions
#
#Copyright (C) 2005 John McFarlane <john.mcfarlane@rockfloatcom>
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
from chula import db

class Test_db(unittest.TestCase):
    """A test class for the db module"""
    
    def setUp(self):
        self.int = 7
        self.str = "foobar"

    def test_clean_bool(self):
        self.assertEqual(db.clean_bool(True), 'TRUE')
        self.assertEqual(db.clean_bool(1), 'TRUE')
        self.assertEqual(db.clean_bool('1'), 'TRUE')
        self.assertEqual(db.clean_bool('true'), 'TRUE')
        self.assertEqual(db.clean_bool('t'), 'TRUE')
        self.assertEqual(db.clean_bool('y'), 'TRUE')
        self.assertEqual(db.clean_bool('On'), 'TRUE')
        self.assertEqual(db.clean_bool(False), 'FALSE')
        self.assertEqual(db.clean_bool(0), 'FALSE')
        self.assertEqual(db.clean_bool('0'), 'FALSE')
        self.assertEqual(db.clean_bool('false'), 'FALSE')
        self.assertEqual(db.clean_bool('f'), 'FALSE')
        self.assertEqual(db.clean_bool('n'), 'FALSE')
        self.assertEqual(db.clean_bool('Off'), 'FALSE')
        self.assertEqual(db.clean_bool(None), 'NULL')
        self.assertEqual(db.clean_bool(''), 'NULL')
        self.assertRaises(ValueError,
                          db.clean_bool,
                          datetime.datetime.now())
    
    def test_clean_date(self):
        self.assertEqual(db.clean_date(None), 'NULL')
        self.assertEqual(db.clean_date(''), 'NULL')
        self.assertEqual(db.clean_date('1/1/2005'), "'1/1/2005'")
        self.assertEqual(db.clean_date('now()', bool_dbfunction=True),
                         'now()')
        # Not leap year
        self.assertEqual(db.clean_date('2/29/2008'), "'2/29/2008'")
        self.assertRaises(ValueError, db.clean_date, 2)
        self.assertRaises(ValueError, db.clean_date, '1/41/2005')
        # Leap year
        self.assertRaises(ValueError, db.clean_date, '2/29/2006')
    
    def test_clean_float(self):
        self.assertEqual(db.clean_float(None), 'NULL')
        self.assertEqual(db.clean_float(35), 35)
        self.assertEqual(db.clean_float('35'), 35)
        self.assertEqual(db.clean_float(35.00), 35.00)
        self.assertEqual(db.clean_float(35.000000001), 35.000000001)
        self.assertEqual(db.clean_float('35.000000001'), 35.000000001)
        self.assertRaises(ValueError, db.clean_float, True)
        self.assertRaises(ValueError, db.clean_float, False)
        self.assertRaises(ValueError, db.clean_float, '35a')
        
    def test_clean_int(self):
        self.assertEqual(db.clean_int(None), 'NULL')
        self.assertEqual(db.clean_int(35), 35)
        self.assertEqual(db.clean_int('35'), 35)
        self.assertEqual(db.clean_int('Null'), 'NULL')
        self.assertRaises(ValueError, db.clean_int, True)
        self.assertRaises(ValueError, db.clean_int, False)
        self.assertRaises(ValueError, db.clean_int, '35a')
    
    def test_clean_str(self):
        clean = db.clean_str
        self.assertEqual(clean('Null'), 'NULL')
        self.assertEqual(clean(''), "''")
        self.assertEqual(clean(""), "''")
        self.assertEqual(clean("''''"), "''''''''''")
        self.assertEqual(clean("b'a"), "'b''a'")
        self.assertEqual(clean("b''a"), "'b''''a'")
        self.assertEqual(clean(r"abc\defg"), r"'abc\\defg'")
        self.assertEqual(clean(r"b\'a"), r"'b\\''a'")
        self.assertEqual(clean("don't"), "'don''t'")
        self.assertEqual(clean("don''t"), "'don''''t'")
        self.assertEqual(clean('a'), "'a'")
        self.assertEqual(clean("a'"), "'a'''")
        self.assertEqual(clean("a'", bool_quote=False), "a''")
        self.assertEqual(clean("a'", bool_quote=False, bool_escape=False), "a'")
        self.assertEqual(clean(None), 'NULL')
        self.assertEqual(clean(5), "'5'")
        self.assertEqual(clean(True), "'True'")
        self.assertEqual(clean(False), "'False'")
    
    def test_clean_tags(self):
        self.assertEqual(db.clean_tags('abc'), "'abc'")
        self.assertEqual(db.clean_tags('Abc'), "'abc'")
        self.assertEqual(db.clean_tags('a b c'), "'a b c'")
        self.assertRaises(ValueError, db.clean_tags, 'abc!')
        self.assertRaises(ValueError, db.clean_tags, None)
        self.assertRaises(ValueError, db.clean_tags, 4)
    
    def test_empty2null(self):
        self.assertEqual(db.empty2null(''), 'NULL')
        self.assertEqual(db.empty2null(""), 'NULL')
        self.assertEqual(db.empty2null('a'), 'a')
        self.assertEqual(db.empty2null(2), 2)
    
def run_unittest():
    # Never change this, leave as is
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    # Replace "example" with the name of your test class and module name
    tests = unittest.makeSuite(Test_db)
    tests.addTest(doctest.DocTestSuite(db))
    return tests

if __name__ == '__main__':
    # Never change this, leave as is
    run_unittest()
