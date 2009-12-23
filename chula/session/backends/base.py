"""Session backend abstract class"""

class Backend(dict):
    def __init__(self, config):
        self.config = config
        self.conn = None

    def connect(self, guid):
        """
        Obtain a datbase connection
        """

        raise NotImplementedError

    def destroy(self, guid):
        """
        Destroy user session

        @param guid: Session guid
        @type guid: chula.guid.guid()
        @return: bool
        """

        raise NotImplementedError

    def fetch_session(self, guid):
        """
        Fetch a user's session from the database.

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

    def persist(self, guid, encoded):
        """
        Persist session

        @param guid: Session guid
        @type guid: chula.guid.guid()
        @param encoded: Data to persist
        @type encoded: str
        @return: bool
        """

        raise NotImplementedError
