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
    """
    Standard Python Queue.Queue with filesystem backing.  It also
    supports key based lookups to fetch the output of message
    processing.
    """

    def __init__(self, config, db=None):
        """
        @param config: Chula configuration
        @type config: chula.config.Config
        @param db: Data store for the messages
        @type db: str (file system path)
        """

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
        """
        Add a new message onto the queue

        @param msg: Message to be added to the queue
        @type msg: chula.queue.messages.message.Message or subclass
        @return: None
        """

        self.persist(msg)
        self.persist_result(msg, None)
        self.put(msg)

    def unprocessed_messages(self, subdir='', suffix='.msg'):
        """
        Allow iteration over messages in the store that have not been
        processed.  This method is only meant to be called when the
        server is not running.  Because a mutex is not used, calling
        this method while the server is running could result in a race
        condition where a given message is processed twice (though not
        likely).  This method is a generator that yields instances of
        chula.queue.messages.message.Message or subclasses of it.

        @param subdir: Directory inside the store to find messages
        @type subdir: str
        @param suffix: File suffix to process, defaults to: ".msg"
        @type suffix: str
        @return: generator
        """

        directory = os.path.join(self.msg_store, subdir)
        for f in os.listdir(directory):
            if f.endswith(suffix):
                msg = message.MessageFactory(open(os.path.join(directory, f)))
                yield msg

    def fetch(self, name):
        """
        Return the result of a message after it was processed

        @param name: Message name
        @type name: str
        @return: Return value of msg.process() or None if not found
        """

        return self.msg_result_store.get(name, None)

    def msg_path(self, name):
        """
        Fetch the filesystem path in the store for a particular
        message.

        @param name: Name of the message (file name)
        @type name: str
        @return: str (fully qualified path, similar to readlink -f)
        """

        return os.path.join(self.msg_store, name)

    def persist(self, msg):
        """
        Persist a message to disk

        @param msg: Message to be persisted to the store
        @type msg: chula.queue.messages.message.Message or subclass
        @return: None
        """

        fmsg = open(self.msg_path(msg.name), 'w')
        fmsg.write(msg.encode())
        fmsg.close()

    def persist_result(self, msg, result):
        """
        Populate a result value into the private message result store.
        This allows a request from the client to request the result of
        message processing.  If enough time has elapsed the result
        might have been purged from the message result store.

        @param msg: Message to be processed
        @type msg: chula.queue.messages.message.Message or subclass
        @param result: Result of message processing
        @type result: The return value of msg.process()
        @return: None
        """

        self.msg_result_store[msg.name] = result

    def mark_in_process(self, msg):
        """
        Mark a given message as being in process

        @param msg: Message to be processed
        @type msg: chula.queue.messages.message.Message or subclass
        @return: bool
        """

        before = os.path.join(self.msg_store, msg.name)
        after = before + '.inprocess'
        os.rename(before, after)

        return msg
        
    def get(self):
        """
        Fetch a message from the queue.  Calling this method also
        marks the message as being in process.

        @return: chula.queue.messages.message.Message or subclass
        """

        msg = super(MessageQueue, self).get()
        self.mark_in_process(msg)

        return msg

    def purge(self, msg, ex=None):
        """
        Move the passed message into the I{processed} location in the
        store.  If there is an exception, persist that into the
        I{failures} location.

        @param msg: Message to be purged
        @type msg: chula.queue.messages.message.Message or subclass
        @param ex: Exception if any
        @type ex: Exception or None
        @return: None
        """

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
            raise message.IOErrorWhenPurgingProcessedMessage(msg)
