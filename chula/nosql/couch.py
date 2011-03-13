"""
Module to extend http://code.google.com/p/couchdb-python/

Usefull links:

- http://wiki.apache.org/couchdb/Introduction_to_CouchDB_views
"""

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
    """
    Obtain a connection to a CouchDB server.

    :param db: Database to connect to
    :type db: :class:`str`
    :param shard: Database shard to use
    :type shard: :class:`str`
    :param server: Database server to use
    :type server: :class:`str`
    :rtype: :class:`couchdb.client.Server`

    .. note::

        The server lookup is in the following order, first match wins:

        #. Value of the ``server`` keyword arg.
        #. :envvar:`CHULA_COUCHDB_SERVER` env variable if set.
        #. http://localhost:5984 as a last resort.

    .. warning::

       CouchDB does not support upper case letters in database names.
       This might save you time :)

       http://wiki.apache.org/couchdb/HTTP_database_API
    """

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
    """CouchDB document abstraction class"""

    def __init__(self, id, **kwargs):
        """
        :param id: Document id (this will be the CouchDB ``_id`` field)
        :type id: :class:`str`
        :param document: Datastructure to clone
        :type document: :class:`dict`
        :param db: Database to connect to
        :type db: :class:`str`
        :param server: Database server to use
        :type server: :class:`str`
        :param shard: Database shard to use
        :type shard: :class:`str`
        :param track_dirty: Only persist to the db when it's actually changed
        :type track_dirty: :class:`bool`
        :rtype: :class:`chula.nosql.couch.Document` (or subclass of)

        .. note::

           For server lookup logic, see :func:`chula.nosql.couch.connect`

        **Example use:**

        >>> from chula.nosql import couch
        >>>
        >>> # Create a couch model class that specifies it's db
        >>> class Foo(couch.Document):
        ...     DB = 'foo'
        >>>
        >>> # Create the new document with some stuff
        >>> f = Foo('abc')
        >>> f['color'] = 'red'
        >>> f['options'] = [1, 2, 3]
        >>> rev = f.persist()
        >>>
        >>> # The document has been persisted, so you can fetch it later
        >>> f = Foo('abc')
        >>> f['options'].pop()
        3

        **Sharding:**

        >>> from chula.nosql import couch
        >>>
        >>> # Create a couch model class that specifies it's db
        >>> class Foo(couch.Document):
        ...     DB = 'foo'
        >>>
        >>> # Create the new document with some stuff
        >>> f = Foo('Marry_Sue', shard='s')
        >>> rev = f.persist()
        >>>
        >>> # The document has been persisted, so you can fetch it later
        >>> f = Foo('Marry_Sue', shard='s')

        **What track_dirty does:**

        >>> import time
        >>> from chula.nosql import couch
        >>>
        >>> # Create a couch model class that specifies it's db
        >>> class Foo(couch.Document):
        ...     DB = 'foo'
        >>>
        >>> doc_id = 'my-uniq-key-%s' % time.time()
        >>>
        >>> # Create the new document
        >>> f = Foo(doc_id)
        >>> rev1 = f.persist()
        >>>
        >>> # Fetch the document from scratch, revision is the same
        >>> f = Foo(doc_id)
        >>> rev1 == f['_rev']
        True
        >>>
        >>> # Persisting the document unmodified doesn't actually talk to
        >>> # the server, nothing has changed
        >>> rev2 = f.persist()
        >>> rev1 == rev2
        True
        >>>
        >>> # Here we will get a new revision because the structure was mutated
        >>> f['new_key'] = {'some-structure':[1, 2, 3, 4]}
        >>> rev4 = f.persist()
        >>> rev2 == rev4
        False
        """

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
        """
        Validate the given document id to make sure it'll be supported
        by CouchDB, and encode as UTF-8.  If the id is not compliant,
        a :class:`chula.nosql.couch.InvalidCouchdbDocumentIdError`
        will be raised.

        :param id: Proposed CouchDB document id
        :type id: :class:`str`
        :rtype: UTF-8 encoded :class:`str`

        >>> from chula.nosql import couch
        >>> couch.Document.sanitize_id('abc')
        'abc'
        """

        if VALID_ID_RE.match(id) is None:
            msg = 'Invalid couchdb document name: "%s", must match: %s'
            raise InvalidCouchdbDocumentIdError(msg % (id, VALID_ID))
        else:
            return id.encode(ENCODING)

    @classmethod
    def delete(self, id, server=None, shard=None):
        """
        Delete the specified document from the specified databse
        (and shard if specified)

        :param id: Document id
        :type id: :class:`str`
        :param server: Database server to use
        :type server: :class:`str`
        :param shard: Database shard to use
        :type shard: :class:`str`
        :rtype: UTF-8 encoded :class:`str`

        >>> from chula.nosql import couch
        >>> class Foo(couch.Document):
        ...     DB = 'foo'
        >>>
        >>> Foo.delete('abc')
        """

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
    """
    CouchDB document abstraction class (plural)
    """

    def __init__(self, server=None, shard=None):
        """
        :param server: Database server to use
        :type server: :class:`str`
        :param shard: Database shard to use
        :type shard: :class:`str`
        :rtype: :class:`None`

        >>> from chula.nosql import couch
        >>>
        >>> class Foo(couch.Document):
        ...     DB = 'foo'
        >>>
        >>> # Now create the plural version of the class
        >>> class Foos(couch.Documents):
        ...     DB = Foo.DB
        """

        super(Documents, self).__init__()
        self.db = connect(self.DB, server=server, shard=shard)
        self.server = server
        self.shard = shard

    def _fill(self, view, cls):
        if not cls is None:
            return [cls(doc.id, document=doc.value) for doc in view]
        else:
            return view

    def query(self, func, cls=None, **kwargs):
        """
        Fetch from CouchDB using an inline query.  This is very
        expensive as the query is compiled on every request.  Only use
        this for development or debugging.  When the query is ready,
        create a view out of it for far improved performance.

        :param func: CouchDB view name
        :type func: :class:`str` (javascript function)
        :type descending: :class:`bool`
        :param limit: Maximum number of documents to return
        :type limit: :class:`int`
        :param startkey: CouchDB view key starting position
        :type startkey: :class:`list`
        :param cls: Class to fill for each document returned by the query
        :type cls: :class:`type`
        :param shard: Database shard to use
        :type shard: :class:`str`
        :rtype: :class:`list` of :class:`chula.nosql.couch.Document` or subclass of it

        >>> from chula.nosql import couch
        >>>
        >>> class Foo(couch.Document):
        ...     DB = 'foo'
        >>>
        >>> # Now create the plural version of the class
        >>> class Foos(couch.Documents):
        ...     DB = Foo.DB
        >>>
        >>> # Create our javascript query function
        >>> query = "function(doc) { emit(null, doc);}"
        >>>
        >>> # Test our shiney adhoc query
        >>> docs = Foos().query(query, cls=Foo)
        >>> doc = docs.pop()
        >>> doc.keys()
        ['new_key', '_rev', '_id', 'modified', 'created']
        >>>
        >>> # A few handy keyword args
        >>> foos = Foos()
        >>> docs = foos.query(query, cls=Foo, limit=3, descending=True)
        >>> len(docs)
        3
        """

        return self._fill(self.db.query(func, **kwargs), cls)

    def view(self, name, cls=None, **kwargs):
        """
        Fetch from a CouchDB view.  Views are by default optimized for
        write performance, thus the first fetch can be slow if data
        has recently changed.

        :param name: CouchDB view name
        :type name: :class:`str`
        :param descending: Sort descending (sorted by view key)
        :type descending: :class:`bool`
        :param limit: Maximum number of documents to return
        :type limit: :class:`int`
        :param startkey: CouchDB view key starting position
        :type startkey: :class:`list`
        :param cls: Class to fill for each document returned by the view
        :type cls: :class:`type`
        :param shard: Database shard to use
        :type shard: :class:`str`

        :rtype: :class:`list` of :class:`chula.nosql.couch.Document` or subclass of it

        >>> from chula.nosql import couch
        >>>
        >>> class Foo(couch.Document):
        ...     DB = 'foo'
        >>>
        >>> # Now create the plural version of the class
        >>> class Foos(couch.Documents):
        ...     DB = Foo.DB
        >>>
        >>> # First let's fetch using a builtin couch view
        >>> docs = Foos().view('_all_docs', cls=Foo)
        >>> len(docs) > 1
        True
        >>> doc = docs.pop()
        >>>
        >>> # A few handy keyword args
        >>> foos = Foos()
        >>> docs = foos.view('_all_docs', cls=Foo, limit=4, descending=True)
        >>> len(docs)
        4
        """

        return self._fill(self.db.view(name, **kwargs), cls)

class DocumentAlreadyExistsError(ResourceNotFound):
    pass

class InvalidCouchdbDocumentIdError(Exception):
    pass
