"""
Class to manage user session.  It is designed to be generic in nature.
"""

from chula import json, memcache
from chula import db, guid
import hashlib

class Session(object):
    """
    The Session class keeps track of user session.
    """
    
    #TODO: The id and HMAC should really be moved
    id = 'chula-session'
    HMAC = 'edf2ccb5711297ebc19cc2f094e2ffc6'
    
    def __init__(self, existing_guid=None, host='localhost', cache=None):
        """
        @param existing_guid: Used to attach to an existing user's session
        @type existing_guid: chula.guid.guid()
        @param host: Specified database hose to use for persistance
        @type host: FQDN
        """

        if guid is None:
            self.guid = guid.guid()
        else:
            self.guid = existing_guid
            
        self.mc = None
        self.conn = None
        self.host = host
        self.status = 'A' # Active

        # Initialize memache client
        if not cache is None:
            self.mc = memcache.Client(cache, debug=0)
        
        # Retrieve session
        self.retrieve()

    def clear(self):
        """
        Clears the session data in the session object
        Justs sets values to an empty dictionary
        """

        self.values = {}
        
    def destroy(self):
        """
        Expire a user's session now.  This does persist to the database
        and memcache immediately.
        """
        
        sql = \
        """
        UPDATE session SET active = FALSE
        WHERE guid = %s;
        """ % db.cstr(self.guid)
        
        # Mark for deletion in the database (maybe do a real delete here)
        self.get_dbConnection()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except db.ProgrammingError, ex:
            self.conn.rollback()
            raise db.ProgrammingError, ex

        # Delete from memcache
        if not self.mc is None:
            self.mc.delete(self.mkey())

    def fetch(self):
        # Ensure that the session dict is of type dict
        if not isinstance(self.values, dict):
            msg = "session.values is not of type dict: %s"
            raise TypeError, msg % self.session.values
        return self.values

    def gc(self):
        """
        Clean up anything related to a user's session, which includes
        database connections B{(might wanna move this elsewhere)}
        """
        
        try:
            self.conn.close()
        except:
            pass
        finally:
            self.conn = None

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
        if not self.record is None:
            self.values = self.record['values']
        else:
            # Session not found in the database, return None and let the
            # caller create a session as it sees fit
            return None

        try:
            self.values = json.decode(self.values)
            return self.values
        except ValueError, ex:
            raise "Unable to json.decode session", ex
    
    def get_dbConnection(self):
        """
        Obtain a datbase connection.
        """
        if self.conn is None:
            self.conn = db.Datastore('pg:chula@%s/chula_session' % self.host)
            self.cursor = self.conn.cursor()

    def get_memcache(self):
        """
        Fetch a user's session from memcache.  If the session isn't found,
        this method will return None

        @return: Native Python object, or None if not found
        """

        values = self.mc.get(self.mkey())
        if not values is None:
            self.values = json.decode(values)
        else:
            self.values = None

        return self.values

    def mkey(self):
        """
        Hash the key to avoid character escaping and the >255 character
        limitation of memcache keys

        @return: SHA1 hash
        """
        
        mc_key = 'session:%s' % self.guid
        return hashlib.sha1(mc_key).hexdigest()
    
    def persist(self):
        """
        Stores session data for later retrieval
        Makes decisions on whether to store long-term or short-term
        Currently long-term is a postgres db, short-term is memcache
        """
        ageKey = 'REQUESTS-BETWEEN-DB-PERSIST'
        self.values[ageKey] = self.values.get(ageKey, -1) + 1

        # Persist to the session state to the database if this is a new
        # session (the ageKey won't be set) or the age (requests between
        # database persists) is greater than a constant value, 10 for
        # now. 
        if self.values[ageKey] == 0 or self.values[ageKey] > 10:
            self.values[ageKey] = 0
            self.forceHardWrite = True
        
        # Ensure that the session dict is of type dict before storing
        if not isinstance(self.values, dict):
            msg = "session.values is not of type dict: %s"
            raise TypeError, msg % self.values

        # Forces a write to the database on the next go
        if self.forceHardWrite is True:
            self.persist_db()

        # Always persist to memcache
        if not self.mc is None:
            self.persist_memcache()

    def persist_db(self):
        """
        Persist the session state to the database.  This method will call
        gc() to garbage collect the session specific database connection
        if it exists.
        """
        
        sql = "SELECT session_set(%s, %s, TRUE);"
        sql = sql % (db.cstr(self.guid),
                     db.cstr(json.encode(self.values)))

        self.get_dbConnection()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except db.ProgrammingError, ex:
            self.conn.rollback()
            raise db.ProgrammingError, ex
        finally:
            # Because persistance is always at the end of the process flow
            # (actually called by the apacheHandler even) we can safely
            # close the database connection now.
            self.gc()

    def persist_memcache(self):
        """
        Persist the session state to memcache.
        """

        timeout = 60 * 30
        timeout = 30 #TODO: Remove this line once we enter production
        self.mc.set(self.mkey(),
                    json.encode(self.values),
                    timeout)

    def retrieve(self):
        """
        Retrieves session data from session storage
        First checks memcache,
        On failure checks database,
        On failure clears session data for a fresh session dict
        """
        # Attempt to pull session from memcache
        # NOTE: get_memcache pulls data into self.session.values --
        #   sessionData here is used only to check the value for None
        if not self.mc is None:
            sessionData = self.get_memcache()
        else:
            sessionData = None

        # If session was not pulled from memcache
        if sessionData is None:
            # Attempt to fill self.session with session data from db
            sessionData = self.get_db()            
            # When set to true, forces the session to be persisted to db
            self.forceHardWrite = True
        else:
            self.forceHardWrite = False
        
        # All attempts at loading session have failed, create empty
        # session
        if sessionData is None:
            self.clear()

