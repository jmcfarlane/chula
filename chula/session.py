"""
Class to manage user session.  It is designed to be generic in nature.
"""

import cPickle
import hashlib

from chula import db, error, guid, json, memcache
from chula.db.datastore import DataStoreFactory

CPICKLE = 'cPickle'
JSON = 'json'
STALE_COUNT = 'REQUESTS-BETWEEN-DB-PERSIST'

class Session(dict):
    """
    The Session class keeps track of user session.
    """
    
    def __init__(self, config, existing_guid=None, transport=CPICKLE):
        """
        Create a user session object

        @param config: Application configuration
        @type config: Instance of chula.config object
        @param existing_guid: Used to attach to an existing user's session
        @type existing_guid: chula.guid.guid()
        """
        
        self._persist_immediately = False
        self._config = config
        self._cache = self._config.session_memcache
        self._timeout = self._config.session_timeout
        self._expired = False
        self._transport = transport

        if existing_guid is None:
            self._guid = guid.guid()
        else:
            self._guid = existing_guid

        # Initialize memache client
        if not isinstance(self._cache, memcache.Client):
            self._cache = memcache.Client(self._cache, debug=0)
        
        # Retrieve session
        self.load()

    def __getattr__(self, key):
        return self.get(key, None)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            self.__dict__[key] = value
        else:
            self[key] = value

    def _gc(self):
        """
        Clean up anything related to a user's session, which includes
        database connections B{(maybe move this elsewhere)}.
        """
        
        try:
            self._conn.close()
        except:
            pass
        finally:
            self._conn = None

    def decode(self, data):
        """
        Decode the session using the specified transport (cPickle by
        default).

        @param data: Session data to be decoded
        @type data: str
        @return: Dict
        """
        if self._transport == CPICKLE:
            return cPickle.loads(data)
        else:
            return json.decode(data)

    def destroy(self):
        """
        Expire a user's session now.  This does persist to the database
        and cache immediately.
        """
        
        sql = "DELETE FROM SESSION WHERE guid = %s;" % db.cstr(self._guid)
        try:
            self.connect_db()
            self._cursor.execute(sql)
            self._conn.commit()
            self.isauthenticated = False
        except:
            self._conn.rollback()
            raise
        finally:
            self._gc()

        # Delete from cache
        if not self._cache is None:
            self._cache.delete(self.mkey())

        # Ensure the data still in memory (self) is not persisted back
        self._expired = True

    def encode(self, data):
        """
        Encode the session using the specified transport (cPickle by
        default).

        @param data: Session data to be encoded
        @type data: Instance of chula.session.Session object
        @return: str
        """

        if self._transport == CPICKLE:
            # Since cPickle actually pickles the entire object we need
            # to exclude all of the private variables prior to encoding:
            return cPickle.dumps(dict(self))
        else:
            return json.encode(data)

    def fetch_from_cache(self):
        """
        Fetch a user's session from cache.  If the session isn't found,
        this method will return None

        @return: Native Python object, or None if not found
        """

        values = self._cache.get(self.mkey())
        if values is None:
            return None
        else:
            return self.decode(values)

    def fetch_from_db(self):
        """
        Fetch a user's session from the database.

        @return: Native Python object, or None if none found
        """

        sql = \
        """
        SELECT values FROM session
        WHERE guid = %s AND active = TRUE;
        """ % (db.cstr(self._guid))
        
        try:
            self.connect_db()
            self._cursor.execute(sql)
            self._record = self._cursor.fetchone()
        except: #self._conn.error.OperationalError, ex:
            return {'SESSION-ERROR':'DATABASE UNAVAILABLE!'}

        if self._record is None:
            return {}
        else:
            try:
                return self.decode(self._record['values'])
            except ValueError, ex:
                raise "Unable to self.decode session", ex
   
    def flush_next_persist(self):
        """
        Persisting to the database does not occur on every request.
        Calling this method forces the very next persist() to force a
        write to the database.  Use this when important session data
        changes and you don't want to risk it being lost.
        """

        self._persist_immediately = True

    def connect_db(self):
        """
        Obtain a datbase connection
        """

        if getattr(self, 'conn', None) is None:
            uri = 'pg:%(session_username)s@%(session_host)s/%(session_db)s'
            uri = uri % self._config
            self._conn = DataStoreFactory(uri, self._config.session_password)
            self._cursor = self._conn.cursor()

    def load(self):
        """
        Fetch session data from cache first, then fall back to the database
        if needed.
        """
        
        data = None
        if not self._cache is None:
            data = self.fetch_from_cache()

        # If the cache is unavailable fetch from the db and be sure to
        # persist to the database as we can't trust the cache currently
        if data is None:
            data = self.fetch_from_db()
            self.flush_next_persist()

        if not data is None:
            self.update(data)

    def mkey(self):
        """
        Hash the key to avoid character escaping and the >255 character
        limitation of cache keys.

        @return: SHA1 hash
        """
        
        mc_key = 'session:%s' % self._guid

        return hashlib.sha1(mc_key).hexdigest()
    
    def persist(self):
        """
        Stores session data for later retrieval Makes decisions on
        whether to store long-term or short-term Currently long-term
        is a postgres db, short-term is cache.
        """

        # Don't do anthing if this session is expired
        if self._expired:
            return

        self[STALE_COUNT] = self.get(STALE_COUNT, -1) + 1

        # Persist to the session state to the database if this is a new
        # session (the STALE_COUNT won't be set) or the age (requests between
        # database persists) is greater than a constant value, 10 for
        # now. 
        if self[STALE_COUNT] == 0 or self[STALE_COUNT] > 10:
            self.flush_next_persist()
        
        # Forces a write to the database on the next go
        if self._persist_immediately:
            self.persist_db()

        # Always persist to cache
        if isinstance(self._cache, memcache.Client):
            self.persist_cache()

    def persist_cache(self):
        """
        Persist the session state to cache
        """

        if self._timeout > 0:
            timeout = self._timeout
        else:
            # Set a reasonable default for cookies lacking an expiration
            timeout = 30

        if isinstance(self._cache, memcache.Client):
            result = self._cache.set(self.mkey(),
                                     self.encode(self),
                                     timeout * 60)
            # Non zero status is success
            if result != 0:
                return True

        return False

    def persist_db(self):
        """
        Persist the session state to the database.  This method will
        call _gc() to garbage collect the session specific database
        connection if it exists.
        """

        # Keep track of what happens
        waspersisted = False
        persist_exception = None
        
        # Indicate a successfull db persist [rollback if necessary]
        current_stale_count = self[STALE_COUNT]
        self[STALE_COUNT] = 0

        # Prepare the sql
        sql = "SELECT session_set(%s, %s, TRUE);"
        sql = sql % (db.cstr(self._guid), db.cstr(self.encode(self)))

        # Attempt the persist
        try:
            self.connect_db()
            self._cursor.execute(sql)
            self._conn.commit()
            waspersisted = True
        except Exception, ex:
            persist_exception = ex
            try:
                self._conn.rollback()
            except:
                pass

            self.flush_next_persist()
            self[STALE_COUNT] = current_stale_count
        finally:
            # Because persistance is always at the end of the process
            # flow (actually called by apache.handler) we can safely
            # close the database connection now, this is the last db
            # work to be done.
            self._gc()

        # If the db persist failed for whatever reason, try to
        # failover on the cache till it comes back up.
        if not waspersisted:
            if self.persist_cache():
                waspersisted = True

        # Raise if we can't persist
        if not waspersisted:
            msg = persist_exception
            raise error.SessionUnableToPersistError(msg)
