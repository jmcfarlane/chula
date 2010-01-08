"""Chula couchdb based session store"""

import os

from chula import data, logger
from chula.nosql import couch
from chula.session.backends import base

LOG = logger.Logger().logger('chula.session.backends.couchdb')

class Backend(base.Backend):
    KEY = 'PICKLE'

    def __init__(self, config, guid):
        super(Backend, self).__init__(config, guid)
        self.server = self.config.session_nosql
        self.doc = None
        self.shard = None

        self.calculate_shard()
        self.connect()

    def connect(self):
        if not self.doc is None:
            return self.doc

        LOG.debug('Connecting with shard: %s' % self.shard)
        self.doc = SessionDoc(self.guid, server=self.server, shard=self.shard)

        return self.doc

    def destroy(self):
        SessionDoc.delete(self.guid, server=self.server, shard=self.shard)

        return True

    def fetch_session(self):
        if self.doc == {}:
            LOG.debug('Document not found: %s' % self.guid)
            return None

        try:
            values = self.doc[self.KEY]
            LOG.debug('Session found: OK')
            return values
        except KeyError, ex:
            LOG.debug('`--> Did not find session data in the document')
        except Exception, ex:
            LOG.error('Error fetching session: ex:%s' % ex)

        return None

    def gc(self):
        self.conn = None

    def persist(self, encoded):
        LOG.debug('persist() called')

        self.doc[self.KEY] = encoded
        persisted = self.doc.persist()
        LOG.debug('Persisted, guid:%s as revision: %s' % (self.guid, persisted))

        return True

    def calculate_shard(self):
        if not self.shard is None:
            return self.shard

        date = data.str2date(self.guid.split('.')[0])
        self.shard = os.path.join(str(date.year), str(date.month))

        return self.shard

class SessionDoc(couch.Document):
    DB = 'chula/session'

