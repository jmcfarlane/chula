# Python imports
from operator import itemgetter
import copy
import os
import re
import time

# Third party imports
import couchdb

# couchdb.http was introduced in 0.7.0
if hasattr(couchdb, 'http'):
    from couchdb.http import ResourceNotFound
else:
    from couchdb import ResourceNotFound

# Project imports
from chula.db import datastore
from chula import collection, logger

CONNECTION_CACHE = {}
ENCODING = 'ascii'
ENV = 'CHULA_COUCHDB_SERVER'
VALID_ID = r'^[-a-zA-Z0-9_.]+$'
VALID_ID_RE = re.compile(VALID_ID)

def connect(db, **kwargs):
    server = kwargs.get('server', None)
    shard = kwargs.get('shard', None)
    futon = None

    if server is None:
        server = os.environ.get(ENV, 'http://localhost:5984')

    # Determine the cache key and serve from cache if possible
    key = (server, db, shard)
    if key in CONNECTION_CACHE:
        return CONNECTION_CACHE[key]

    # Create fresh connection to the db, and cache it
    futon = datastore.DataStoreFactory('couchdb:%s' % server)
    if shard is None:
        conn = futon.db(db)
    else:
        conn = futon.db(os.path.join(db, shard))

    CONNECTION_CACHE[key] = conn

    return conn

class Document(dict):
    """
    CouchDB document abstraction class
    """

    def __init__(self, id, **kwargs):
        document = kwargs.get('document', None)

        # Member variables
        self.db_conn = kwargs.get('db_conn', None)
        self.server = kwargs.get('server', None)
        self.shard = kwargs.get('shard', None)
        self.track_dirty = kwargs.get('track_dirty', True)

        super(Document, self).__init__()

        if not self.db_conn is None:
            self.db = self.db_conn
        else:
            self.db = connect(self.DB, server=self.server, shard=self.shard)

        # If this is a couchdb document, just fill - don't fetch
        try:
            self.fill(id, document)
        except TypeError:
            try:
                self.fill(self.db[id]['_id'], self.db[id])
            except ResourceNotFound, ex:
                self.fill(id, {})
        except:
            raise

        # Allow keeping track of is_dirty
        if self.track_dirty:
            # Avoid a direct deepcopy on self, as we indirectly have a
            # lock via the connection attributes.  Casting back to a
            # dict makes this clean, but removes attribute access.
            # Using a chula.collection.Collection gives this back
            self._copy = collection.Collection(copy.deepcopy(dict(self)))
            self._copy.id = self.id

        # Loggers use thread locks and thus can't be copied
        self.log = logger.Logger().logger('chula.nosql.couch')

    @staticmethod
    def sanitize_id(id):
        if VALID_ID_RE.match(id) is None:
            msg = 'Invalid couchdb document name: "%s", must match: %s'
            raise InvalidCouchdbDocumentIdError(msg % (id, VALID_ID))
        else:
            return id.encode(ENCODING)

    @classmethod
    def delete(self, id, server=None, shard=None):
        id = self.sanitize_id(id)
        db = connect(self.DB, server=server, shard=shard)

        try:
            del db[id] 
        except ResourceNotFound:
            pass

    def fill(self, id, data):
        self.id = self.sanitize_id(id)
        self.update(data)
        
    def is_dirty(self):
        if self._copy is None:
            return True

        for key, value in self.iteritems():
            if self._copy.get(key, '__MISSING__') != value:
                return True

        if self.id != self._copy.id:
            return True

        return False

    def persist(self):
        # Make sure the id has not been made invalid
        self.id = self.sanitize_id(self.id)

        # Support new documents
        if self.get('_rev', None) is None:
            self['created'] = time.time()
            self.db[self.id] = self

        # Support existing documents
        elif self.is_dirty():
            # Support document renames
            if not self._copy is None and self.id != self._copy.id:
                try:
                    del self.db[self._copy.id]
                except ResourceNotFound, ex:
                    msg = 'Rename attempt failed (must be a unique id)'
                    raise DocumentAlreadyExistsError(msg)

                # Since couchdb sees this as a del/add - remove the _rev
                del self['_rev']

            self['modified'] = time.time()
            self.db[self.id] = self
            return self.db[self.id]['_rev']

        return self['_rev']

class Documents(list):
    def __init__(self, server=None, shard=None):
        super(Documents, self).__init__()
        self.db = connect(self.DB, server=server, shard=shard)
        self.server = server
        self.shard = shard

    def _fill(self, view, cls):
        if not cls is None:
            return [cls(doc.id, doc.value) for doc in view]
        else:
            return view

    def query(self, func, cls=None, **kwargs):
        return self._fill(self.db.query(func, **kwargs), cls)

    def view(self, name, cls=None, **kwargs):
        return self._fill(self.db.view(name, **kwargs), cls)

class DocumentAlreadyExistsError(ResourceNotFound):
    pass

class InvalidCouchdbDocumentIdError(Exception):
    pass
