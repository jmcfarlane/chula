"""Chula postgresql based session store"""

# Project imports
from chula import db, logger
from chula.db.datastore import DataStoreFactory
from chula.session.backends import base

EXTRA = {'clientip':''}

class Backend(base.Backend):
    def __init__(self, config, guid):
        super(Backend, self).__init__(config, guid)
        self.cursor = None
        self.log = logger.Logger(config).logger('chula.session.postgresql')

        self.connect()

    def connect(self):
        if self.conn is None:
            uri = 'pg:%(session_username)s@%(session_host)s/%(session_db)s'
            uri = uri % self.config
            try:
                self.conn = DataStoreFactory(uri, self.config.session_password)
            except Exception, ex:
                self.log.error('Unable to connect', exc_info=True, extra=EXTRA)

            try:
                self.cursor = self.conn.cursor()
            except Exception, ex:
                self.log.error('Cursor error', exc_info=True, extra=EXTRA)

            if not self.conn is None and not self.cursor is None:
                self.log.debug('Successfull connection to postgresql')

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
        self.log.debug('fetching data from postgresql')

        sql = "SELECT values FROM session WHERE guid = %s AND active = TRUE;"
        sql = sql % db.cstr(self.guid)

        row = None

        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
        except Exception, ex: #self.conn.error.OperationalError, ex:
            self.log.warning('guid: %s', self.guid, exc_info=True, extra=EXTRA)
            return None

        if row is None:
            self.log.debug('No active session, guid: %s' % self.guid)
            return None
        else:
            self.log.debug('Session found: OK')
            return row['values']

    def gc(self):
        try:
            self.conn.close()
        except:
            pass
        finally:
            self.conn = None

    def persist(self, encoded):
        self.log.debug('persist() called')

        sql = "SELECT session_set(%s, %s, TRUE);"
        sql = sql % (db.cstr(self.guid), db.cstr(encoded))

        # Attempt the persist
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            self.log.debug('Persisted: OK')
            return True
        except Exception, ex:
            try:
                self.conn.rollback()
            except:
                pass

        # If we get here - persist failed
        return False
