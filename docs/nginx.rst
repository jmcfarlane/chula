.. _nginx_fastcgi:

=================
Nginx via FastCGI
=================

The first step in FastCGI_ integration, is to create the application
server that Nginx_ will sent requests to.  For this example, we'll use
a unix domain socket, rather than TCP/IP for connectivity between the
two.

FastCGI process
^^^^^^^^^^^^^^^

Create :file:`myapp/fastcgi.py`::

 try:
     from flup.server.fcgi_fork import WSGIServer
 except ImportError:
     from chula.vendor.fcgi import WSGIServer
     print "Unable to import flup.server.fcgi import WSGIServer"
     print " >>> Falling back on old version available in Chula"

 from chula.www.adapters.fcgi import adapter

 # Expose the myapp, as it's not "installed"
 sys.path.insert(0, os.getcwd())

 from model import configuration

 @adapter.fcgi
 def application():
     return configuration.app

 # Start the server which will handle calls from the webserver
 WSGIServer(application, bindAddress='/tmp/myapp.socket').run()

Start up the FastCGI_ process::

 python myapp/fastcgi.py

Make sure Nginx has permissions to write to the socket::

 chmod o+w /tmp/myapp.socket

TODO: Provide an example init script to properly startup the socket,
setting permissions and what not.

Nginx config
^^^^^^^^^^^^

Configure Nginx_ to proxy application requests to our
application.  Add this to the ``server`` block of your Nginx_
configuration::

 # Send all requests without a file extension to myapp:
 location ~ ^([a-z/_])+$ {
   # This is needed when using Ubuntu
   include /etc/nginx/fastcgi_params;

   # FastCGI parameter settings
   fastcgi_read_timeout 3m;
   fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
   fastcgi_param SERVER_ADMIN NA;
   fastcgi_param SERVER_SIGNATURE nginx/$nginx_version;

   # The path to our running unix domain socket
   server unix:/tmp/myapp.socket;
 }

Restart Nginx_ ::

 sudo /etc/init.d/nginx restart

Try it!
^^^^^^^

Now you should be able to hit: http://your-server/myapp/blog

.. _FastCGI: http://en.wikipedia.org/wiki/FastCGI
.. _Nginx: http://nginx.org
