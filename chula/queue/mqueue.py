"""
Chula message queue
"""

import Queue
import cPickle
import os
import shutil

from chula import collection
from chula.queue.messages import message

class MessageQueue(Queue.Queue, object):
    def __init__(self, config, db=None):
        super(MessageQueue, self).__init__()

        self._msg_store_iter = None
        if db is None:
            self.db = config.mqueue_db
        else:
            self.db = db

        # Where do we keep the actual messages on disk
        self.msg_store = os.path.join(self.db, 'msgs')

        # Create a location to store the message processing output
        self.msg_result_store = collection.UboundCollection(1024)

        # Make sure the db dir exists, creating it if necessary
        for directory in ['', 'processed', 'failures']:
            try:
                os.makedirs(os.path.join(self.msg_store, directory))
            except OSError, er:
                if str(er).startswith('[Errno 17] File exists'):
                    pass
                else:
                    raise

    def add(self, msg):
        self.persist(msg)
        self.persist_result(msg, None)
        self.put(msg)

    def fetch_msg_store_iter(self, subdir='', suffix='.msg'):
        directory = os.path.join(self.msg_store, subdir)
        for f in os.listdir(directory):
            if f.endswith(suffix):
                yield os.path.join(directory, f)

    def fetch(self, name):
        return self.msg_result_store.get(name, None)

    def msg_path(self, name, ext=''):
        return os.path.join(self.msg_store, name)

    def persist(self, msg):
        fmsg = open(self.msg_path(msg.name), 'w')
        fmsg.write(msg.encode())
        fmsg.close()

    def persist_result(self, msg, result):
        self.msg_result_store[msg.name] = result

    def process(self, msg):
        before = os.path.join(self.msg_store, msg['name'])
        after = before + '.inprocess'
        os.rename(before, after)
        msg = message.MessageFactory(open(after, 'r'))

        return msg
        
    def get(self):
        msg = super(MessageQueue, self).get()

        return self.process(msg)

    def purge(self, msg, ex=None):
        if ex is None:
            folder = 'processed'
        else:
            folder = 'failures'
            elog = os.path.join(self.msg_store, folder, msg.name + '.cpickle')
            elog = open(elog, 'w')
            cPickle.dump(ex, elog)
            elog.close()
        try:
            fpath = self.msg_path(msg.name + '.inprocess')
            dest = os.path.join(self.msg_store, folder, msg.name)
            shutil.move(fpath, dest)
        except IOError, er:
            msg = 'The message was not marked as being processed'
            raise message.CannotPurgeUnprocessedError(msg)
