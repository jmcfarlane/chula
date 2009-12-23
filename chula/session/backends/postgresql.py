"""Chula postgresql based session store"""

from chula import db, logger
from chula.db.datastore import DataStoreFactory
from chula.session.backends import base

LOG = logger.Logger().logger('chula.session.backends.postgresql')

class Backend(base.Backend):
    def __init__(self, config, guid):
        super(Backend, self).__init__(config, guid)
        self.cursor = None

        self.connect()

    def connect(self):
        if self.conn is None:
            uri = 'pg:%(session_username)s@%(session_host)s/%(session_db)s'
            uri = uri % self.config
            try:
                self.conn = DataStoreFactory(uri, self.config.session_password)
            except Exception, ex:
                LOG.error('Unable to connect to postgresql: %s' % ex)

            try:
                self.cursor = self.conn.cursor()
            except Exception, ex:
                LOG.error('Unable to create postgresql cursor: %s' % ex)

            if not self.conn is None and not self.cursor is None:
                LOG.debug('Successfull connection to postgresql')

    def destroy(self):
        sql = "DELETE FROM SESSION WHERE guid = %s;" % db.cstr(self.guid)

        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            raise

        return False

    def fetch_session(self):
        LOG.debug('fetching data from postgresql')

        sql = "SELECT values FROM session WHERE guid = %s AND active = TRUE;"
        sql = sql % db.cstr(self.guid)

        row = None

        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
        except Exception, ex: #self.conn.error.OperationalError, ex:
            LOG.warning('SQL error guid: %s, ex:%s' % (self.guid, ex))
            return None

        if row is None:
            LOG.debug('`--> No active session, guid: %s' % self.guid)
            return None
        else:
            LOG.debug('Session found: OK')
            return row['values']
   
    def gc(self):
        try:
            self.conn.close()
        except:
            pass
        finally:
            self.conn = None

    def persist(self, encoded):
        LOG.debug('persist() called')

        sql = "SELECT session_set(%s, %s, TRUE);"
        sql = sql % (db.cstr(self.guid), db.cstr(encoded))

        # Attempt the persist
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            LOG.debug('Persisted: OK')
            return True
        except Exception, ex:
            try:
                self.conn.rollback()
            except:
                pass

        # If we get here - persist failed
        return False
