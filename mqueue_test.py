# Test the queue
from chula import collection
from chula.queue import mqueue 

config = collection.Collection()
config.mqueue_db = 'sqlite:memory'
queue = mqueue.MessageQueue(config)


# Test the messages
from chula.queue.messages import message

msg = message.MessageFactory('email')
print msg.__class__
