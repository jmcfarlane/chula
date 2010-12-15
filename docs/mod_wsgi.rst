=================
WSGI via Mod_WSGI
=================

Mod_WSGI_ is the best choice if you want to run your app on Apache_.
This configuration also happens is a little easier to setup.

WSGI handler
^^^^^^^^^^^^

Create :file:`myapp/wsgi.py`, which will be loaded by Mod_WSGI_ ::

 import os
 import sys
 from chula.www.adapters.wsgi import adapter

 # Expose the myapp, as it's not "installed"
 sys.path.insert(0, '/var/www/myapp')

 from model import configuration

 @adapter.wsgi
 def application():
     return configuration.app

Apache config
^^^^^^^^^^^^^

Add this to your ``VirtualHost``::

 WSGIScriptAliasMatch ^([a-z/_])+$ /path/to/myapp/wsgi.py 

Try it!
^^^^^^^

Restart Apache::

 sudo /etc/init.d/apache restart

Now you should be able to hit: http://your-server/myapp/blog

.. _Apache: http://www.apache.org
.. _Mod_WSGI: http://code.google.com/p/modwsgi/
