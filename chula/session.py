"""
Class to manage user session.  It is designed to be generic in nature.
"""

from chula import db, guid, json, memcache
import hashlib

class Session(dict):
    """
    The Session class keeps track of user session.
    """
    
    #TODO: The id and HMAC should really be moved
    id = 'chula-session'
    HMAC = 'edf2ccb5711297ebc19cc2f094e2ffc6'
    
    def __init__(self, config, _guid=None):
        """
        @param existing_guid: Used to attach to an existing user's session
        @type existing_guid: chula.guid.guid()
        @param host: Specified database hose to use for persistance
        @type host: FQDN
        """
        
        self.config = config
        self.cache = self.config.session_memcache
        self.persistImmediately = False

        if _guid is None:
            self.guid = guid.guid()
        else:
            self.guid = _guid

        # Initialize memache client
        if not self.cache is None:
            #TODO: Add type checking here
            self.cache = memcache.Client(self.cache, debug=0)
        
        # Retrieve session
        self.populate()

    def __getattr__(self, key):
        return self.get(key, None)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def destroy(self):
        """
        Expire a user's session now.  This does persist to the database
        and cache immediately.
        """
        
        sql = "DELETE FROM SESSION WHERE guid = %s;" % db.cstr(self.guid)
        self.get_dbConnection()
        try:
            self.cursor.execute(sql)
            self.conn.commit()

        except db.ProgrammingError, ex:
            self.conn.rollback()
            raise

        # Delete from cache
        if not self.cache is None:
            self.cache.delete(self.mkey())

    def populate(self):
        """
        Fetch session data from cache first, then fall back to the datbase
        if needed.
        """
        
        if not self.cache is None:
            data = self.get_cache()

        if data is None:
            data = self.get_db()

        if not data is None:
            self.update(data)

    def gc(self):
        """
        Clean up anything related to a user's session, which includes
        database connections B{(maybe move this elsewhere)}.
        """
        
        try:
            self.conn.close()
        except:
            pass
        finally:
            self.conn = None

    def get_cache(self):
        """
        Fetch a user's session from cache.  If the session isn't found,
        this method will return None

        @return: Native Python object, or None if not found
        """

        values = self.cache.get(self.mkey())
        if values is None:
            return None
        else:
            return json.decode(values)

    def get_db(self):
        """
        Fetch a user's session from the database.

        @return: Native Python object, or None if none found
        """
        sql = \
        """
        SELECT values FROM session
        WHERE guid = %s AND active = TRUE;
        """ % (db.cstr(self.guid))
        
        self.get_dbConnection()
        self.cursor.execute(sql)
        self.record = self.cursor.fetchone()
        if self.record is None:
            return {}
        else:
            try:
                return json.decode(self.record['values'])
            except ValueError, ex:
                raise "Unable to json.decode session", ex
    
    def get_dbConnection(self):
        """
        Obtain a datbase connection.
        """

        if getattr(self, 'conn', None) is None:
            #TODO: Fix Collection() to support '%(foo)s'
            config = {}
            config['session_host'] = self.config.session_host
            config['session_db'] = self.config.session_db
            uri = 'pg:chula@%(session_host)s/%(session_db)s' % config
            self.conn = db.Datastore(uri)
            self.cursor = self.conn.cursor()

    def mkey(self):
        """
        Hash the key to avoid character escaping and the >255 character
        limitation of cache keys

        @return: SHA1 hash
        """
        
        mc_key = 'session:%s' % self.guid
        return hashlib.sha1(mc_key).hexdigest()
    
    def persist(self):
        """
        Stores session data for later retrieval
        Makes decisions on whether to store long-term or short-term
        Currently long-term is a postgres db, short-term is cache
        """
        ageKey = 'REQUESTS-BETWEEN-DB-PERSIST'
        self[ageKey] = self.get(ageKey, -1) + 1

        # Persist to the session state to the database if this is a new
        # session (the ageKey won't be set) or the age (requests between
        # database persists) is greater than a constant value, 10 for
        # now. 
        if self[ageKey] == 0 or self[ageKey] > 10:
            self[ageKey] = 0
            self.persistImmediately = True
        
        # Forces a write to the database on the next go
        if self.persistImmediately is True:
            self.persist_db()

        # Always persist to cache
        if not self.cache is None:
            self.persist_cache()

    def persist_db(self):
        """
        Persist the session state to the database.  This method will call
        gc() to garbage collect the session specific database connection
        if it exists.
        """
        
        sql = "SELECT session_set(%s, %s, TRUE);"
        sql = sql % (db.cstr(self.guid), db.cstr(json.encode(self)))

        self.get_dbConnection()
        try:
            self.cursor.execute(sql)
            self.conn.commit()

        except db.ProgrammingError, ex:
            self.conn.rollback()
            raise

        finally:
            # Because persistance is always at the end of the process flow
            # (actually called by the apacheHandler even) we can safely
            # close the database connection now :)
            self.gc()

    def persist_cache(self):
        """
        Persist the session state to cache.
        """

        timeout = 60 * 30
        timeout = 30 #TODO: Remove this line once we enter production
        self.cache.set(self.mkey(), json.encode(self), timeout)

