"""Chula Postgresql datastore object"""

import re

from chula import error

try:
    import psycopg2
    from psycopg2 import extensions, extras

    # We want unicode objects, makes life much easier
    # See: http://www.initd.org/psycopg/docs/usage.html#unicode-handling
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
except:
    raise error.MissingDependencyError('Psycopg2')

from chula.db.engines import engine

class DataStore(engine.Engine):
    """
    Postgresql engine class using the Psycopg2 driver
    """

    def __init__(self, uri, passwd='', *args, **kwargs):
        super(DataStore, self).__init__()
        m = re.match(r'(?P<user>[-a-zA-Z0-9]+)@'
                     r'(?P<host>[-a-zA-Z0-9]+)/'
                     r'(?P<db>[-a-zA-Z0-9_]+)$', uri)

        if m is None:
            raise error.MalformedConnectionStringError(engine)

        parts = m.groupdict()
        parts['pass'] = passwd

        conn = 'host=%(host)s dbname=%(db)s user=%(user)s password=%(pass)s'
        self.conn = psycopg2.connect(conn % parts)

        # Expose the psycopg2 exceptions
        self.error.DataError = psycopg2.DataError
        self.error.DatabasError = psycopg2.DatabaseError
        self.error.Error = psycopg2.Error
        self.error.IntegrityError = psycopg2.IntegrityError
        self.error.InterfaceError = psycopg2.InterfaceError
        self.error.InternalError = psycopg2.InternalError
        self.error.NotSupportedError = psycopg2.NotSupportedError
        self.error.OperationalError = psycopg2.OperationalError
        self.error.ProgrammingError = psycopg2.ProgrammingError

    def set_isolation(self, level=1):
        """
        Toggle the isolation level. Here are the available
        isolation levels:
            - 0 = No isolation
            - 1 = READ COMMITTED (the default)
            - 3 = SERIALIZABLE

        @param level: Isolation level
        @type level: Integer
        """

        self.conn.set_isolation_level(level)

    def cursor(self, type='dict'):
        """
        Create database cursor

        @param type: Type of cursor to return
        @type type: string, I{dict} or I{tuple}
        @return: Instance
        """

        if type == 'tuple':
            return self.conn.cursor(cursor_factory=psycopg2.extensions.cursor)

        elif type == 'dict':
            return self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        else:
            msg = 'Invalid cursor type, use either tuple or dict'
            raise error.UnsupportedUsageError(append=msg)
