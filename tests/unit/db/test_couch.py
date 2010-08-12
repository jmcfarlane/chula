# Python imports
import os
import time
import unittest

# Third party imports
import couchdb

# couchdb.http was introduced in 0.7.0
if hasattr(couchdb, 'http'):
    from couchdb.http import ResourceNotFound
else:
    from couchdb import ResourceNotFound

# Project imports
from chula.error import *
from chula.db import datastore
from chula.db.engines import couch
from chula.nosql import couch as couch_document

SANDBOX = 'sandbox'
SERVER = 'http://localhost:5984'

class SampleDocument(couch_document.Document):
    DB = SANDBOX

class SampleDocuments(couch_document.Documents):
    DB = SANDBOX

class Test_couchdb(unittest.TestCase):
    doctest = couch

    def setUp(self):
        self.futon = datastore.DataStoreFactory('couchdb:%s' % SERVER)

    def tearDown(self):
        pass

    def connect(self, db=SANDBOX):
        self.db = self.futon.db(db)

    def test_connection_type(self):
        self.assertTrue(isinstance(self.futon.conn, couchdb.Server))

    def test_connection_with_existing_db(self):
        self.connect()
        self.assertTrue(isinstance(self.db, couchdb.Database))

    def test_connection_with_new_db(self):
        TEST = 'chula_datastore_test_%s' % str(time.time()).split('.')[0]
        self.connect(TEST)
        self.assertTrue(isinstance(self.db, couchdb.Database))
        self.futon.delete(TEST)

class Test_couchdb_document(unittest.TestCase):
    doctest = couch_document

    def setUp(self):
        self.futon = datastore.DataStoreFactory('couchdb:%s' % SERVER)

    def tearDown(self):
        pass

    def connect(self, db=SANDBOX):
        self.db = self.futon.db(db)

    def test_document(self):
        NAME = 'foobar'
        doc = SampleDocument(NAME, server=SERVER)
        doc['test'] = 'testing'
        doc.persist()

        doc = SampleDocument(NAME, server=SERVER)
        doc['test'] = 'testing again'
        doc.persist()

    def test_document_using_env_var(self):
        os.environ[couch_document.ENV] = SERVER
        doc = SampleDocument('foobar')
        doc.persist()

    def test_documents(self):
        func = """
            function (doc) {
                emit(doc._id, doc)
            }
        """

        for doc in SampleDocuments(server=SERVER).query(func):
            self.assertTrue(isinstance(doc, dict))
