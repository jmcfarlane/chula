import unittest

from chula import config
from chula.queue import mqueue
from chula.queue.messages import echo, mail, message

config = config.Config()

class Test_mqueue(unittest.TestCase):
    doctest = message

    def _add(self, module=echo):
        msg = module.Message()
        msg.message = 'payload'
        self.mqueue.add(msg)

    def setUp(self):
        self.mqueue = mqueue.MessageQueue(config)

    def tearDown(self):
        pass
        #self.mqueue.close()

    #def test_schema(self):
    #    self.assertEquals(True, self.mqueue.schema_exists())

    def test_add(self):
        self._add()

    #def test_add_empty_email(self):
    #    mtype = 'email'
    #    msg = message.MessageFactory(mtype)
    #    self.assertEquals(mtype, msg.type)
    #    self.failIf(isinstance(msg, email.Message) is False)

    #def test_add_dict(self):
    #    mtype = 'email'
    #    msg = {}
    #    msg['id'] = 0
    #    msg['message'] = 'foobar'
    #    msg['name'] = 'foobar'
    #    msg['inprocess'] = True
    #    msg['processed'] = False
    #    msg['type'] = mtype
    #    msg['created'] = '5/4/1971 14:00:00'
    #    msg['updated'] = '5/4/1971 14:00:00'
    #    
    #    msg = message.MessageFactory(msg)
    #    self.assertEquals(mtype, msg.type)
    #    self.failIf(isinstance(msg, email.Message) is False)

    #def test_pop_returns_message(self):
    #    self._add()
    #    msg = self.mqueue.pop()
    #    self.failIf(msg is None)
    #    
    #def test_pop_return_msg_with_correct_fields(self):
    #    keys_expected = ['id',
    #                     'message',
    #                     'name',
    #                     'inprocess',
    #                     'processed',
    #                     'type',
    #                     'created',
    #                     'updated']
    #    keys_expected.sort()

    #    self._add()
    #    msg = self.mqueue.pop()
    #    keys_found = msg.keys()
    #    keys_found.sort()
    #    self.assertEquals(keys_expected, keys_found)
    #    self.assertEquals(True, isinstance(msg, message.Message))

    #def test_pop_setting_inprocess(self):
    #    self._add()
    #    msg = self.mqueue.pop()
    #    self.assertEquals(True, msg.inprocess)

    #def test_cannot_purge_unprocessed(self):
    #    self._add()
    #    msg = self.mqueue.pop()

    #    # Force the processed flag to False
    #    msg.inprocess = False
    #    self.mqueue.persist(msg)

    #    self.assertRaises(message.IOErrorWhenPurgingProcessedMessage,
    #                      self.mqueue.purge, msg)

    #def test_successfull_purge(self):
    #    self._add()
    #    msg = self.mqueue.pop()
    #    msg = self.mqueue.purge(msg)
    #    msg = self.mqueue.pop()
    #    self.assertEquals(None, msg)
