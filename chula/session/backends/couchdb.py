"""Chula couchdb based session store"""

# Python imports
import os

# Project imports
from chula import data, logger
from chula.nosql import couch
from chula.session.backends import base

EXTRA = {'clientip':''}

class Backend(base.Backend):
    KEY = 'PICKLE'

    def __init__(self, config, guid):
        super(Backend, self).__init__(config, guid)
        self.server = self.config.session_nosql
        self.doc = None
        self.log = logger.Logger(config).logger('chula.session.couchdb')

        self.shard = None

        self.calculate_shard()
        self.connect()

    def connect(self):
        if not self.doc is None:
            return self.doc

        self.log.debug('Connecting with shard: %s' % self.shard)
        try:
            self.doc = SessionDoc(self.guid,
                                  server=self.server,
                                  shard=self.shard)
            return self.doc
        except Exception, ex:
            self.log.error('Unable to connect', exc_info=True, extra=EXTRA)
            return None

    def destroy(self):
        if self.doc is None:
            self.log.error('Unable to destroy', exc_info=True, extra=EXTRA)
            return False

        SessionDoc.delete(self.guid, server=self.server, shard=self.shard)

        return True

    def fetch_session(self):
        if self.doc == {}:
            self.log.debug('Document not found: %s' % self.guid)
            return None

        try:
            values = self.doc[self.KEY]
            self.log.debug('Session found: OK')
            return values
        except KeyError, ex:
            self.log.debug('Did not find session data in the document')
        except Exception, ex:
            self.log.error('Error fetching session', exc_info=True, extra=EXTRA)

        return None

    def gc(self):
        self.conn = None

    def persist(self, encoded):
        self.log.debug('persist() called')

        if self.doc is None:
            self.log.error('Unable to persist: no db connection', extra=EXTRA)
            return False

        self.doc[self.KEY] = encoded
        persisted = self.doc.persist()
        self.log.debug('saved guid:%s, revision: %s' % (self.guid, persisted))

        return True

    def calculate_shard(self):
        if not self.shard is None:
            return self.shard

        date = data.str2date(self.guid.split('.')[0])
        self.shard = os.path.join(str(date.year), str(date.month))

        return self.shard

class SessionDoc(couch.Document):
    DB = 'chula/session'

