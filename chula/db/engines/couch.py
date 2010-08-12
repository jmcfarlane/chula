# Third party imports
import couchdb

# couchdb.http was introduced in 0.7.0
if hasattr(couchdb, 'http'):
    from couchdb.http import PreconditionFailed, ResourceNotFound
else:
    from couchdb import PreconditionFailed, ResourceNotFound

# Project imports
from chula.db.engines import engine

class DataStore(engine.Engine):
    """
    CouchDB engine class
    """

    def __init__(self, uri, *args, **kwargs):
        super(DataStore, self).__init__()
        self.conn = couchdb.Server(uri)

    def delete(self, db):
        try:
            del self.conn[db]
        except ResourceNotFound, ex:
            pass

    def db(self, db):
        try:
            return self.conn[db]
        except ResourceNotFound, ex:
            try:
                return self.conn.create(db)
            except PreconditionFailed, ex:
                # Work around the situation where a client/server
                # mismatch results in a PreconditionFailed error being
                # raised, even when it was actually created
                # successfully.  Remove this maybe in time.
                if db in self.conn:
                    return self.conn[db]
                else:
                    raise
