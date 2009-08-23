"""
db functions unit tests
"""

#test_functions.py - Class to test generic python functions
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
import datetime

from chula.db import functions as fcn
from chula.db.engines import postgresql, sqlite
from chula.db.datastore import DataStoreFactory
from chula.error import *

class Test_functions(unittest.TestCase):
    """A test class for the db module"""

    doctest = fcn
    
    def _DS(self, conn):
        return DataStoreFactory(conn)

    def setUp(self):
        self.int = 7
        self.str = "foobar"

    def test_cbool(self):
        self.assertEqual(fcn.cbool(True), 'TRUE')
        self.assertEqual(fcn.cbool(1), 'TRUE')
        self.assertEqual(fcn.cbool('1'), 'TRUE')
        self.assertEqual(fcn.cbool('true'), 'TRUE')
        self.assertEqual(fcn.cbool('t'), 'TRUE')
        self.assertEqual(fcn.cbool('y'), 'TRUE')
        self.assertEqual(fcn.cbool('On'), 'TRUE')
        self.assertEqual(fcn.cbool(False), 'FALSE')
        self.assertEqual(fcn.cbool(0), 'FALSE')
        self.assertEqual(fcn.cbool('0'), 'FALSE')
        self.assertEqual(fcn.cbool('false'), 'FALSE')
        self.assertEqual(fcn.cbool('f'), 'FALSE')
        self.assertEqual(fcn.cbool('n'), 'FALSE')
        self.assertEqual(fcn.cbool('Off'), 'FALSE')
        self.assertEqual(fcn.cbool(None), 'NULL')
        self.assertEqual(fcn.cbool(''), 'NULL')
        self.assertRaises(TypeConversionError,
                          fcn.cbool,
                          datetime.datetime.now())
    
    def test_cdate(self):
        self.assertEqual(fcn.cdate(None), 'NULL')
        self.assertEqual(fcn.cdate(''), 'NULL')
        self.assertEqual(fcn.cdate('1/1/2005'), "'1/1/2005'")
        self.assertEqual(fcn.cdate('now()', isfunction=True), 'now()')

        # Date with time
        self.assertEqual(fcn.cdate('1/1/2005 10:00:00'), "'1/1/2005 10:00:00'")
        self.assertEqual(fcn.cdate('1-1-2005 10:00:00'), "'1-1-2005 10:00:00'")
        self.assertEqual(fcn.cdate('2005-1-1 10:00:00'), "'2005-1-1 10:00:00'")
        self.assertEqual(fcn.cdate('2008-7-16 5:50:20'), "'2008-7-16 5:50:20'")

        # Not leap year
        self.assertEqual(fcn.cdate('2/29/2008'), "'2/29/2008'")
        self.assertRaises(TypeConversionError, fcn.cdate, 2)
        self.assertRaises(TypeConversionError, fcn.cdate, '1/41/2005')

        # Leap year
        self.assertRaises(TypeConversionError, fcn.cdate, '2/29/2006')
    
    def test_cfloat(self):
        self.assertEqual(fcn.cfloat(None), 'NULL')
        self.assertEqual(fcn.cfloat(''), 'NULL')
        self.assertEqual(fcn.cfloat(35), 35)
        self.assertEqual(fcn.cfloat('35'), 35)
        self.assertEqual(fcn.cfloat(35.00), 35.00)
        self.assertEqual(fcn.cfloat(35.000000001), 35.000000001)
        self.assertEqual(fcn.cfloat('35.000000001'), 35.000000001)
        self.assertEqual(fcn.cfloat(True), 1.0)
        self.assertEqual(fcn.cfloat(False), 0.0)
        self.assertRaises(TypeConversionError, fcn.cfloat, '35a')
        
    def test_cint(self):
        self.assertEqual(fcn.cint(None), 'NULL')
        self.assertEqual(fcn.cint(''), 'NULL')
        self.assertEqual(fcn.cint(35), 35)
        self.assertEqual(fcn.cint(True), 1)
        self.assertEqual(fcn.cint(False), 0)
        self.assertEqual(fcn.cint('35'), 35)
        self.assertEqual(fcn.cint('Null'), 'NULL')
        self.assertRaises(TypeConversionError, fcn.cint, '35a')
    
    def test_connection_factory_postgresql(self):
        conn = DataStoreFactory('pg:chula@localhost/chula_test', 'chula')
        self.assertEquals(True, isinstance(conn, postgresql.DataStore))

    def test_connection_factory_sqlite(self):
        conn = self._DS('sqlite:/tmp/chula_sqlite_test.db')
        self.assertEquals(True, isinstance(conn, sqlite.DataStore))

    def test_connection_string_invalid_type(self):
        conn = 'oracle:localhost/chula_test'
        self.assertRaises(UnsupportedDatabaseEngineError, self._DS, conn)

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
        clean = fcn.cstr
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
    
    def test_cregex(self):
        self.assertEqual(fcn.cregex(r'.*'), "'.*'")
        self.assertEqual(fcn.cregex(r''), "''")
        self.assertEqual(fcn.cregex(r'.*', doquote=False), ".*")
        self.assertRaises(TypeConversionError, fcn.cregex, '[')
        self.assertRaises(TypeConversionError, fcn.cregex, None)

    def test_ctags(self):
        self.assertEqual(fcn.ctags(''), "NULL")
        self.assertEqual(fcn.ctags(None), "NULL")
        self.assertEqual(fcn.ctags('abc'), "'abc'")
        self.assertEqual(fcn.ctags('Abc'), "'abc'")
        self.assertEqual(fcn.ctags('a b c'), "'a b c'")
        self.assertEqual(fcn.ctags(['c', 'b', 'a']), "'a b c'")
        self.assertRaises(TypeConversionError, fcn.ctags, 'abc!')
        self.assertRaises(TypeConversionError, fcn.ctags, 4)
    
    def test_datatore_basic(self):
        conn = DataStoreFactory('pg:chula@localhost/chula_test', 'chula')
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
        conn = DataStoreFactory('pg:chula@localhost/chula_test', 'chula')
        cursor = conn.cursor(type='tuple')
        try:
            cursor.execute('SELECT * FROM cars LIMIT 1;')
            values = cursor.fetchone()
            self.assertEquals(values, (1, 'Honda', 'Civic'))
        finally:
            conn.rollback()
            conn.close()

    def test_empty2null(self):
        self.assertEqual(fcn.empty2null(''), 'NULL')
        self.assertEqual(fcn.empty2null(""), 'NULL')
        self.assertEqual(fcn.empty2null('a'), 'a')
        self.assertEqual(fcn.empty2null(2), 2)

    def test_invalid_cursor(self):
        conn = DataStoreFactory('pg:chula@localhost/chula_test', 'chula')
        self.assertRaises(UnsupportedUsageError, conn.cursor, type='list')
        conn.close()

    def test_unquote(self):
        self.assertEqual(fcn.unquote("'abc'"), "abc")
        self.assertEqual(fcn.unquote('"abc"'), '"abc"')
        self.assertEqual(fcn.unquote("'ABC'"), "ABC")
        self.assertEqual(fcn.unquote("'a'bc'"), "a'bc")
        self.assertEqual(fcn.unquote("'a\"bc'"), "a\"bc")
        self.assertEqual(fcn.unquote("'x'"), "x")
        self.assertEqual(fcn.unquote("abc"), "abc")
        self.assertEqual(fcn.unquote(None), None)
        self.assertEqual(fcn.unquote(5), 5)
        self.assertEqual(fcn.unquote('5'), '5')
