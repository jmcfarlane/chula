from operator import itemgetter
import copy
import os
import re
import time

from couchdb import client, ResourceNotFound

from chula.db import datastore
from chula import logger

CONNECTION_CACHE = {}
ENCODING = 'ascii'
ENV = 'CHULA_COUCHDB_SERVER'
VALID_ID = r'^[-a-zA-Z0-9_.]+$'
VALID_ID_RE = re.compile(VALID_ID)

def connect(db, server=None, shard=None):
    futon = None

    if server is None:
        server = os.environ.get(ENV, None)

    if server is None:
        msg = 'Server uri not specified'
        raise Exception(msg)

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

    def __init__(self, id,
                 db_conn=None,
                 document=None,
                 server=None,
                 shard=None,
                 track_dirty=True):

        super(Document, self).__init__()

        if not db_conn is None:
            self.db = db_conn
        else:
            self.db = connect(self.DB, server=server, shard=shard)

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
        if track_dirty:
            self._copy = copy.deepcopy(self)
        else:
            track_dirty = None

        # Loggers use thread locks and thus can't be copied
        self.log = logger.Logger().logger('chula.nosql.couch')

    @staticmethod
    def sanitize_id(id):
        if VALID_ID_RE.match(id) is None:
            msg = 'Invalid couchdb document name: "%s", must match: %s'
            raise InvalidCouchdbDocumentId(msg % (id, VALID_ID))
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

    def query(self, func, cls=None, sort=False, reverse=False):
        view = self.db.query(func)

        # Fill the requested class types if desired
        if not cls is None:
            view = [cls(doc.key, doc.value) for doc in view]

        # Sort if desired
        if sort:
            view.sort(reverse=reverse)

        return view

    def view(self, name, cls=None, sort=False, reverse=False):
        view = self.db.view(name)

        # Fill the requested class types if desired
        if not cls is None:
            view = [cls(doc.key, doc.value) for doc in view]

        # Sort if desired
        if sort:
            view.sort(reverse=reverse)

        return view

class DocumentAlreadyExistsError(ResourceNotFound):
    pass

class InvalidCouchdbDocumentId(Exception):
    pass
