"""Chula couchdb based session store"""

import os

from chula import data, logger
from chula.nosql import couch
from chula.session.backends import base

LOG = logger.Logger().logger('chula.session.backends.couchdb')

class Backend(base.Backend):
    _key = 'PICKLE'

    def fetch_session(self, guid):
        doc = self.connect(guid)

        try:
            return doc[self._key]
        except KeyError, ex:
            LOG.debug('`--> did not find any data in the db')

        except Exception, ex:
            LOG.error('unable to fetch session, guid: %s, ex:%s' % (guid, ex))
            raise "Unable to self.decode session", ex

        return None
   
    def connect(self, guid):
        shard = self.shard(guid)
        LOG.debug('Connecting with shard: %s' % shard)

        return SessionDocument(guid, server=self.config.session_nosql, shard=shard)

    def destroy(self, guid):
        shard = self.shard(guid)
        SessionDocument.delete(guid, server=self.config.session_nosql, shard=shard)

        return True

    def gc(self):
        self.conn = None

    def persist(self, guid, encoded):
        LOG.debug('persist called')

        doc = self.connect(guid)
        doc[self._key] = encoded
        doc.persist()

        return True

    def shard(self, guid):
        date = data.str2date(guid.split('.')[0])
        return os.path.join(str(date.year), str(date.month))

class SessionDocument(couch.Document):
    DB = 'chula/session'

