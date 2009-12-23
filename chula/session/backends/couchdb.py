"""Chula couchdb based session store"""

import os

from chula import data, logger
from chula.nosql import couch
from chula.session.backends import base

LOG = logger.Logger().logger('chula.session.backends.couchdb')

class Backend(base.Backend):
    _key = 'PICKLE'

    def __init__(self, config):
        super(Backend, self).__init__(config)
        self.couch_uri = self.config.session_nosql

    def fetch_session(self, guid):
        doc = self.connect(guid)
        if doc == {}:
            LOG.debug('Document not found: %s' % guid)
            return None

        try:
            values = doc[self._key]
            LOG.debug('Session found: OK')
            return values
        except KeyError, ex:
            LOG.debug('`--> Did not find session data in the document')
        except Exception, ex:
            LOG.error('Unable to fetch session, guid: %s, ex:%s' % (guid, ex))

        return None
   
    def connect(self, guid):
        shard = self.shard(guid)
        LOG.debug('Connecting with shard: %s' % shard)

        return SessionDocument(guid, server=self.couch_uri, shard=shard)

    def destroy(self, guid):
        shard = self.shard(guid)
        SessionDocument.delete(guid, server=self.couch_uri, shard=shard)

        return True

    def gc(self):
        self.conn = None

    def persist(self, guid, encoded):
        LOG.debug('persist() called')

        doc = self.connect(guid)
        doc[self._key] = encoded
        persisted = doc.persist()
        LOG.debug('Persisted, guid:%s as revision: %s' % (guid, persisted))

        return True

    def shard(self, guid):
        date = data.str2date(guid.split('.')[0])
        return os.path.join(str(date.year), str(date.month))

class SessionDocument(couch.Document):
    DB = 'chula/session'

