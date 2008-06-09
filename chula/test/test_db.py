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
from chula.error import *

class Test_db(unittest.TestCase):
    """A test class for the db module"""
    
    def _DS(self, conn):
        return db.Datastore(conn)

    def setUp(self):
        self.int = 7
        self.str = "foobar"

    def test_cbool(self):
        self.assertEqual(db.cbool(True), 'TRUE')
        self.assertEqual(db.cbool(1), 'TRUE')
        self.assertEqual(db.cbool('1'), 'TRUE')
        self.assertEqual(db.cbool('true'), 'TRUE')
        self.assertEqual(db.cbool('t'), 'TRUE')
        self.assertEqual(db.cbool('y'), 'TRUE')
        self.assertEqual(db.cbool('On'), 'TRUE')
        self.assertEqual(db.cbool(False), 'FALSE')
        self.assertEqual(db.cbool(0), 'FALSE')
        self.assertEqual(db.cbool('0'), 'FALSE')
        self.assertEqual(db.cbool('false'), 'FALSE')
        self.assertEqual(db.cbool('f'), 'FALSE')
        self.assertEqual(db.cbool('n'), 'FALSE')
        self.assertEqual(db.cbool('Off'), 'FALSE')
        self.assertEqual(db.cbool(None), 'NULL')
        self.assertEqual(db.cbool(''), 'NULL')
        self.assertRaises(TypeConversionError,
                          db.cbool,
                          datetime.datetime.now())
    
    def test_cdate(self):
        self.assertEqual(db.cdate(None), 'NULL')
        self.assertEqual(db.cdate(''), 'NULL')
        self.assertEqual(db.cdate('1/1/2005'), "'1/1/2005'")
        self.assertEqual(db.cdate('now()', isfunction=True), 'now()')

        # Not leap year
        self.assertEqual(db.cdate('2/29/2008'), "'2/29/2008'")
        self.assertRaises(TypeConversionError, db.cdate, 2)
        self.assertRaises(TypeConversionError, db.cdate, '1/41/2005')

        # Leap year
        self.assertRaises(TypeConversionError, db.cdate, '2/29/2006')
    
    def test_cfloat(self):
        self.assertEqual(db.cfloat(None), 'NULL')
        self.assertEqual(db.cfloat(''), 'NULL')
        self.assertEqual(db.cfloat(35), 35)
        self.assertEqual(db.cfloat('35'), 35)
        self.assertEqual(db.cfloat(35.00), 35.00)
        self.assertEqual(db.cfloat(35.000000001), 35.000000001)
        self.assertEqual(db.cfloat('35.000000001'), 35.000000001)
        self.assertEqual(db.cfloat(True), 1.0)
        self.assertEqual(db.cfloat(False), 0.0)
        self.assertRaises(TypeConversionError, db.cfloat, '35a')
        
    def test_cint(self):
        self.assertEqual(db.cint(None), 'NULL')
        self.assertEqual(db.cint(''), 'NULL')
        self.assertEqual(db.cint(35), 35)
        self.assertEqual(db.cint(True), 1)
        self.assertEqual(db.cint(False), 0)
        self.assertEqual(db.cint('35'), 35)
        self.assertEqual(db.cint('Null'), 'NULL')
        self.assertRaises(TypeConversionError, db.cint, '35a')
    
    def test_connection_string_format(self):
        conn = self._DS('pg:chula@localhost/chula_test')
        self.assertEquals(True, isinstance(conn, db.Datastore))

    def test_connection_string_invalid_type(self):
        conn = 'mysql:localhost/chula_test'
        self.assertRaises(MalformedConnectionStringError, self._DS, conn)

    def test_connection_string_missing_user(self):
        conn = 'pg:localhost/chula_test'
        self.assertRaises(MalformedConnectionStringError, self._DS, conn)
    
    def test_connection_string_missing_host(self):
        conn = 'pg:chula/chula_test'
        self.assertRaises(MalformedConnectionStringError, self._DS, conn)

    def test_connection_string_missing_db(self):
        conn = 'pg:chula@localhost'
        self.assertRaises(MalformedConnectionStringError, self._DS, conn)
    
    def test_cstr(self):
        clean = db.cstr
        self.assertEqual(clean(None), 'NULL')
        self.assertEqual(clean('Null'), "'Null'")
        self.assertEqual(clean('NULL'), "'NULL'")
        self.assertEqual(clean(''), "''")
        self.assertEqual(clean(""), "''")
        self.assertEqual(clean("''''"), "''''''''''")
        self.assertEqual(clean("b'a"), "'b''a'")
        self.assertEqual(clean("b''a"), "'b''''a'")
        self.assertEqual(clean(r"abc\defg"), r"'abc\\defg'")
        self.assertEqual(clean(r"b\a"), r"'b\\a'")
        self.assertEqual(clean(r"b\'a"), r"'b\\''a'")
        self.assertEqual(clean("don't"), "'don''t'")
        self.assertEqual(clean("don''t"), "'don''''t'")
        self.assertEqual(clean('a'), "'a'")
        self.assertEqual(clean("a'"), "'a'''")
        self.assertEqual(clean("a'", doquote=False), "a''")
        self.assertEqual(clean("a'", doquote=False, doescape=False), "a'")
        self.assertEqual(clean(5), "'5'")
        self.assertEqual(clean(True), "'True'")
        self.assertEqual(clean(False), "'False'")
    
    def test_ctags(self):
        self.assertEqual(db.ctags(''), "NULL")
        self.assertEqual(db.ctags(None), "NULL")
        self.assertEqual(db.ctags('abc'), "'abc'")
        self.assertEqual(db.ctags('Abc'), "'abc'")
        self.assertEqual(db.ctags('a b c'), "'a b c'")
        self.assertEqual(db.ctags(['c', 'b', 'a']), "'a b c'")
        self.assertRaises(TypeConversionError, db.ctags, 'abc!')
        self.assertRaises(TypeConversionError, db.ctags, 4)
    
    def test_datatore_basic(self):
        conn = db.Datastore('pg:chula@localhost/chula_test')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM cars LIMIT 1;')
            keys = cursor.fetchone().keys()
            keys.sort()
            self.assertEquals(keys, ['make', 'model', 'uid'])
        finally:
            conn.rollback()
            conn.close()

    def test_datatore_tuple(self):
        conn = db.Datastore('pg:chula@localhost/chula_test')
        cursor = conn.cursor(type='tuple')
        try:
            cursor.execute('SELECT * FROM cars LIMIT 1;')
            values = cursor.fetchone()
            self.assertEquals(values, (1, 'Honda', 'Civic'))
        finally:
            conn.rollback()
            conn.close()

    def test_empty2null(self):
        self.assertEqual(db.empty2null(''), 'NULL')
        self.assertEqual(db.empty2null(""), 'NULL')
        self.assertEqual(db.empty2null('a'), 'a')
        self.assertEqual(db.empty2null(2), 2)

    #def test_extreme_danger_exception(self):
    #    conn = db.Datastore('pg:chula@localhost/chula_test')
    #    cursor = conn.cursor()
    #    try:
    #        sql = 'DELETE FROM cars;'
    #        self.assertRaises(ExtremeDangerError, cursor.execute, sql)
    #    finally:
    #        conn.rollback()
    #        conn.close()
        
    def test_invalid_cursor(self):
        conn = db.Datastore('pg:chula@localhost/chula_test')
        self.assertRaises(UnsupportedUsageError, conn.cursor, type='list')
        conn.close()

    def test_unquote(self):
        self.assertEqual(db.unquote("'abc'"), "abc")
        self.assertEqual(db.unquote('"abc"'), '"abc"')
        self.assertEqual(db.unquote("'ABC'"), "ABC")
        self.assertEqual(db.unquote("'a'bc'"), "a'bc")
        self.assertEqual(db.unquote("'a\"bc'"), "a\"bc")
        self.assertEqual(db.unquote("'x'"), "x")
        self.assertEqual(db.unquote("abc"), "abc")
        self.assertEqual(db.unquote(None), None)
        self.assertEqual(db.unquote(5), 5)
        self.assertEqual(db.unquote('5'), '5')
            
def run_unittest():
    unittest.TextTestRunner(verbosity=2).run(get_tests())

def get_tests():
    tests = unittest.makeSuite(Test_db)
    tests.addTest(doctest.DocTestSuite(db))
    return tests

if __name__ == '__main__':
    run_unittest()
