"""Session backend abstract class"""

class Backend(dict):
    def __init__(self, config, guid):
        self.config = config
        self.guid = guid
        self.conn = None

    def connect(self):
        """
        Obtain a connection to the backend
        """

        raise NotImplementedError

    def destroy(self):
        """
        Destroy user session

        @param guid: Session guid
        @type guid: chula.guid.guid()
        @return: bool
        """

        raise NotImplementedError

    def fetch_session(self):
        """
        Fetch a user's session from the backend

        @param guid: Session guid
        @type guid: chula.guid.guid()
        @return: dict, or None
        """

        raise NotImplementedError
   
    def gc(self):
        """
        Clean up datastore connection
        """

        raise NotImplementedError

    def persist(self, encoded):
        """
        Persist session

        @param guid: Session guid
        @type guid: chula.guid.guid()
        @param encoded: Data to persist
        @type encoded: str
        @return: bool
        """

        raise NotImplementedError
