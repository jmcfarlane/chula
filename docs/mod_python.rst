=====================
Apache via Mod_python
=====================

Mod_PYTHON_ was the first way to run Python applications under Apache
with excellent performance.  It's still awesome, though Mod_WSGI_ has
superceeded it.

Mod_python handler
^^^^^^^^^^^^^^^^^^

Create :file:`myapp/mod_python.py`, which will be loaded by Mod_PYTHON_ ::

 from chula.www.adapters.mod_python import adapter
 from model import configuration
 
 @adapter.handler
 def handler():
     return configuration.app

Apache config
^^^^^^^^^^^^^

Update your apache ``VirtualHost`` to have::

 <Directory /path/to/myapp>
   PythonDebug On
   PythonHandler mod_python
   PythonPath "['/path/to/myapp'] + sys.path"
   SetHandler python-program
 </Directory>

Try it!
^^^^^^^

Restart Apache::

 sudo /etc/init.d/apache restart

Now you should be able to hit: http://your-server/myapp/blog

.. _Apache: http://www.apache.org
.. _Mod_python: http://www.modpython.org
.. _Mod_WSGI: http://code.google.com/p/modwsgi/
