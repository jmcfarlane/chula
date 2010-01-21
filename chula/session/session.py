"""Chula session factory"""

import cPickle

from chula import json, logger
from chula.session.backends import memcached

CPICKLE = 'cPickle'
JSON = 'json'
STALE_COUNT = 'REQUESTS-BETWEEN-DB-PERSIST'
SESSION_UNAVAILABLE = 'SESSION_IS_CURRENTLY_UNAVAILABLE'

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
        @param transport: Storage format for session data
        @type transport: str ('cPickle' or 'json')
        """

        # Create member variables
        self._config = config
        self._expired = False
        self._log = logger.Logger(config).logger('chula.session')
        self._max_stale_count = config.session_max_stale_count
        self._persist_immediately = False
        self._timeout = config.session_timeout
        self._transport = transport

        # Establish a guid
        if existing_guid is None:
            self._guid = guid.guid()
        else:
            self._guid = existing_guid

        # Determine the backend to use
        if not self._config.session_nosql is None:
            from chula.session.backends import couchdb
            self._backend =  couchdb.Backend(self._config, self._guid)
        else:
            from chula.session.backends import postgresql
            self._backend = postgresql.Backend(self._config, self._guid)

        # Always use a memcached backend
        self._cache = memcached.Backend(self._config, self._guid)

        # Set global session defaults
        self.isauthenticated = False

        # Retrieve session
        self.load()

    def __getattr__(self, key):
        """
        Support attribute style accessor
        """

        return self.get(key, None)

    def __setattr__(self, key, value):
        """
        Support attribute style mutator
        """

        if key.startswith('_'):
            self.__dict__[key] = value
        else:
            self[key] = value

    def _gc(self):
        """
        Clean up anything related to a user's session, which includes
        backend connections.
        """

        self._log.debug('session._gc() called')
        
        self._backend.gc()
        self._cache.gc()
    
    def decode(self, data):
        """
        Decode the session using the specified transport (cPickle by
        default).

        @param data: Session data to be decoded
        @type data: str
        @return: Dict
        """
        
        # Detect already decoded data
        if data is None:
            return None # TODO: Is this the right thing to do?
        elif isinstance(data, dict):
            return data

        # Decode using the desired transport
        if self._transport == CPICKLE:
            return cPickle.loads(data)
        else:
            return json.decode(data)

    def destroy(self):
        """
        Expire a user's session now.  This does persist to the database
        and cache immediately.
        """
        
        self._backend.destroy()
        self._cache.destroy()

        # Ensure the data still in memory (self) is not persisted back
        self._expired = True
        self.isauthenticated = False

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

    def load(self):
        """
        Fetch session data from cache first, then fall back to the
        backend if needed.
        """

        self._log.debug('Fetching session, guid:%s' % self._guid)
        
        data = None

        # Fetch session from cache first
        if not self._cache is None:
            data = self.decode(self._cache.fetch_session())

        # If the cache is unavailable fetch from the db and be sure to
        # persist to the database as we can't trust the cache currently
        if data is None:
            self._log.debug('`--> stale_count: %s' % self.get(STALE_COUNT))
            data = self.decode(self._backend.fetch_session())

        if data is None:
            msg = 'Active session not found in cache or backend, guid:%s'
            self._log.debug(msg % self._guid)

            # Either the backends are unavailable, or this is a brand
            # new session, either way persist asap
            self.flush_next_persist()
        else:
            self.update(data)
    
        self._log.debug('User session now loaded with the following k/v pairs:')
        for key, value in self.iteritems():
            self._log.debug('`--> %s: %s' % (key, value))

    def flush_next_persist(self):
        """
        Persisting to the database does not occur on every request.
        Calling this method forces the very next persist() to force a
        write to the database.  Use this when important session data
        changes and you don't want to risk it being lost.
        """
        
        self._log.debug('flush_next_persist called')

        self._persist_immediately = True

    def persist(self):
        """
        Stores session data for later retrieval Makes decisions on
        whether to store long-term or short-term Currently long-term
        is a postgres db, short-term is cache.
        """

        # Don't do anthing if this session is expired
        if self._expired:
            return

        # Set and increment the stale count.  If unset, it's inital
        # value is set to -2, then incremented so it winds up being
        # set to -1 if initially unset.  A value of -1 results in the
        # first commit of session hitting the cache, the second hits
        # the db - after that it's based on the max_stale_count.
        self[STALE_COUNT] = self.get(STALE_COUNT, -2) + 1

        self._log.debug('stale_count in persist(): %s' % self[STALE_COUNT])

        # Persist the session state to the database if this is a new
        # session (the STALE_COUNT won't be set) or the age (requests
        # between database persists) is greater than a constant value,
        # 10 for now. 
        if self[STALE_COUNT] == 0 or self[STALE_COUNT] > self._max_stale_count:
            self._log.debug('decision made to call flush_next_persist')
            self.flush_next_persist()

        # Save the stale count in case the backend persist fails, then
        # mark the session as no longer stale (restore if persist
        # fails)
        current_stale_count = self[STALE_COUNT]
        self[STALE_COUNT] = 0
        
        # Create encoded session using the desired transport
        encoded = self.encode(self)

        # Persist to the backend if needed
        if self._persist_immediately:
            if self._backend.persist(encoded):
                self._persist_immediately = False
            else:
                self[STALE_COUNT] = current_stale_count
                self.flush_next_persist()

        # Always persist to cache
        persisted = self._cache.persist(encoded)
