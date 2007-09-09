"""
Session service (wrapper) class
"""

from chula.services.baseService
from chula import session

class SessionService(baseService.BaseService):
    def __init__(self, guid=None):
        # Get session object with initialized guid
        self.session = session.Session(guid)

        # Retrieve session
        self.retrieve()

    def values(self):
        # Ensure that the session dict is of type dict
        if not isinstance(self.session.values, dict):
            msg = "session.values is not of type dict: %s"
            raise TypeError, msg % self.session.values
        return self.session.values

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
        sessionData = self.session.get_memcache()

        # If session was not pulled from memcache
        if sessionData is None:
            # Attempt to fill self.session with session data from db
            sessionData = self.session.get_db()            
            # When set to true, forces the session to be persisted to db
            self.forceHardWrite = True
        else:
            self.forceHardWrite = False
        
        # All attempts at loading session have failed, create empty
        # session
        if sessionData is None:
            self.session.clear()

    def persist(self):
        """
        Stores session data for later retrieval
        Makes decisions on whether to store long-term or short-term
        Currently long-term is a postgres db, short-term is memcache
        """

        ageKey = 'REQUESTS-BETWEEN-DB-PERSIST'
        self.session.values[ageKey] = self.session.values.get(ageKey, -1) + 1

        # Persist to the session state to the database if this is a new
        # session (the ageKey won't be set) or the age (requests between
        # database persists) is greater than a constant value, 10 for
        # now. 
        if self.session.values[ageKey] == 0 or self.session.values[ageKey] > 10:
            self.session.values[ageKey] = 0
            self.forceHardWrite = True
        
        # Ensure that the session dict is of type dict before storing
        if not isinstance(self.session.values, dict):
            msg = "session.values is not of type dict: %s"
            raise TypeError, msg % self.session.values

        # Forces a write to the database on the next go
        if self.forceHardWrite is True:
                self.session.persist_db()

        # Always persist to memcache
        self.session.persist_memcache()
