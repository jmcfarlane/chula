"""
Chula message queue
"""

import os

from chula import collection
from chula.queue.messages import message

class MessageQueue(object):
    def __init__(self, config, db=None):
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
        # Update the message to indicate this thread did the work
        thread_id = id(msg)
        msg.id = thread_id
        msg.name = msg.msg_name()

        self.persist(msg)

    def list(self):
        msgs = []

        for f in os.listdir(self.msg_store):
            if f.endswith('.msg'):
                msg = file.open(self.msg_path(f), 'r').readlines()
                msgs.append(message.MessageFactory(''.join(msg)))

        return msgs

    def msg_path(self, name, ext=''):
        return os.path.join(self.msg_store, name)

    def persist(self, msg):
        fmsg = open(self.msg_path(msg.name), 'w')
        fmsg.write(msg.encode())
        fmsg.close()

    def pop(self):
        msg = None
        for f in os.listdir(self.msg_store):
            if f.endswith('.msg'):
                before = self.msg_path(f)
                after = before + '.inprocess'
                os.rename(before, after)
                msg = open(after, 'r')

                break

        if not msg is None:
            msg = message.MessageFactory(msg)

        return msg

    def purge(self, msg):
        try:
            os.remove(self.msg_path(msg.name + '.inprocess'))
        except OSError, er:
            msg = 'The messagage was not marked as being processed'
            raise message.CannotPurgeUnprocessedError(msg)
