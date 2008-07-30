"""
Chula message queue
"""

import os

from chula import collection
from chula.queue.messages import message

class MessageQueue(object):
    def __init__(self, config, db=None):
        self._msg_store_iter = None
        if db is None:
            self.db = config.mqueue_db
        else:
            self.db = db

        # Where do we keep the actual messages on disk
        self.msg_store = os.path.join(self.db, 'msgs')

        # Make sure the db dir exists, creating it if necessary
        try:
            os.makedirs(self.msg_store)
        except OSError, er:
            if str(er).startswith('[Errno 17] File exists'):
                pass
            else:
                raise

    def add(self, msg):
        self.persist(msg)

    def fetch_msg_store_iter(self):
        for f in os.listdir(self.msg_store):
            if f.endswith('.msg'):
                yield self.msg_path(f)

    def msg_path(self, name, ext=''):
        return os.path.join(self.msg_store, name)

    def persist(self, msg):
        fmsg = open(self.msg_path(msg.name), 'w')
        fmsg.write(msg.encode())
        fmsg.close()

    def pop(self):
        # If necessary fetch a fresh file iterator
        if self._msg_store_iter is None:
            self._msg_store_iter = self.fetch_msg_store_iter()

        try:
            f = self._msg_store_iter.next()
            after = f + '.inprocess'
            os.rename(f, after)
            msg = message.MessageFactory(open(after, 'r'))
        except StopIteration:
            self._msg_store_iter = None
            msg = None

        return msg

    def purge(self, msg):
        try:
            os.remove(self.msg_path(msg.name + '.inprocess'))
        except OSError, er:
            msg = 'The messagage was not marked as being processed'
            raise message.CannotPurgeUnprocessedError(msg)
