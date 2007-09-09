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
    HMAC = 'td3g4d9-gb19fmxs.edf9zalqdfyedsew67'
    
    def __init__(self, _guid=None, host='session.chula.db'):
        """
        @param _guid: Used to attach to an existing user's session
        @type _guid: chula.guid.guid()
        @param host: Specified database hose to use for persistance
        @type host: FQDN
        """

        if guid is None:
            self.guid = guid.guid()
        else:
            self.guid = _guid
            
        self.conn = None
        self.host = host
        self.status = 'A' # Active

        # Initialize memache client
        self.mc = memcache.Client(memcache.HOSTS_session, debug=0)
        
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
            logger.debug("Session gc'd")
            self.conn = None
    
    def destroy(self):
        """
        Expire a user's session now.  This does persist to the database
        and memcache immediately.
        """
        
        
        sql = \
        """
        UPDATE session SET active = FALSE
        WHERE guid = %s;
        """ % db.clean_str(self.guid)
        
        # Mark for deletion in the database (maybe do a real delete here)
        self.get_dbConnection()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            logger.debug('session destroyed itself')
        except db.ProgrammingError, ex:
            self.conn.rollback()
            logger.exception(   "session couldn't destroy itself, " + \
                               "rolledback session information")
            raise db.ProgrammingError, ex

        # Delete from memcache
        self.mc.delete(self.mkey())

    def clear(self):
        """
        Clears the session data in the session object
        Justs sets values to an empty dictionary
        """

        self.values = {}
        
    def get_db(self):
        """
        Fetch a user's session from the database.

        @return: Native Python object, or None if none found
        """
        sql = \
        """
        SELECT values FROM session
        WHERE guid = %s AND active = TRUE;
        """ % (db.clean_str(self.guid))
        
        self.get_dbConnection()
        self.cursor.execute(sql)
        self.record = self.cursor.fetchone()
        if not self.record is None:
            self.values = self.record['values']
        else:
            # Session not found in the database, return None and let the
            # caller create a session as it sees fit
            logger.debug('Session not found in database.')
            return None

        try:
            self.values = json.decode(self.values)
            return self.values
        except ValueError, ex:
            logger.exception("Unable to json.decode session")
            raise "Unable to json.decode session", ex
    
    def get_dbConnection(self):
        """
        Obtain a datbase connection.
        """
        if self.conn is None:
            logger.debug(   "Creating db connection: pg:session@%s/session" \
                            % self.host)
            self.conn = db.Datastore('pg:session@%s/session' % self.host)
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
            logger.debug("Session info not found in memcache, looking up in db")

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
    
    def persist_db(self):
        """
        Persist the session state to the database.  This method will call
        gc() to garbage collect the session specific database connection
        if it exists.
        """
        
        sql = "SELECT session_set(%s, %s, TRUE);"
        sql = sql % (db.clean_str(self.guid),
                     db.clean_str(json.encode(self.values)))

        self.get_dbConnection()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except db.ProgrammingError, ex:
            self.conn.rollback()
            logger.exception("Couldn't persist session info to db")
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
