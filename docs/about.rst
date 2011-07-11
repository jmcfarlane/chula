===========
About Chula
===========

History
+++++++

Chula is written by John McFarlane (aka me).  When I first wanted to learn
Python I started a project named *Apple*.  At the time there were lots
of frameworks for building web applications with Python, but I was
interested in learning Python so it seemed more fun to make my own.
Additionally I was surprised by the complexity of other frameworks.  I
was looking for something a bit simpler.

I hacked on Apple for a few years, and then decided to start over and
try to improve things based on what I had learned - 3 months later I
released the first version of Chula.  Since that time I've tried to
improve things and add features as needed, but I never lost sight of
it's main purpose: to be a vehicle for me to have fun and learn stuff.

If you're really wanting to build the next killer application I'd
prolly recommend using `Django <http://djangoproject.org>`__.  If
you're looing for something smaller or even just something *different*
then give Chula a try :)

Features
++++++++

* Web servers: Most of the common setups are supported (Mod_Python_,
  Mod_WSGI_, and FastCGI_).
* Session: Uses both Memcached_ and PostgreSQL_ for cluster safe
  storage that scales pretty well.
* Message queue: Support for asynchronous processing of messages
* Typical stuff: Environment, GET and POST variables
* Speed: Chula seems to perform pretty well

Dependencies
++++++++++++

Chula depends on the following packages, some of which are optional
depending on configuration:

Mandatory
~~~~~~~~~

#. Python_ (2.5, 2.6 or 2.7)

.. NOTE:: Python-3.1 builds are available, but are considered unstable

Optional
~~~~~~~~

* CouchDB_ and the couchdb-python_ driver
* Flup_ (If using FastCGI this is recommended, but still optional)
* Mako_ (Optional but recommended)
* Memcached_
* PostgreSQL_ and the Psycopg2_ driver
* Web server: Nginx_, Apache_, etc.

If you intend on enabling support for session, you will need
Memcached, and either PostgreSQL or CouchDB and their respective
drivers.  You can learn more about session `here <session.html>`_.

Source code
+++++++++++

Chula uses the Git_ version control system.  The official Chula repository
can be found on Github_.

Issue tracker
+++++++++++++

Chula uses the issue tracker that's integrated with Github_.  If you
find defects or have ideas for improvement please feel free to file
issues.  In the event Chula becomes more popular, a more sophisticated
tracker will be used.

The link to the Github tracker is here:
http://github.com/jmcfarlane/chula/issues

Release cycle
+++++++++++++

Generally there are about 4 releases a year

Roadmap
+++++++

The roadmap right now is pretty small.  Here are the features I'm
currently thinking about:

1. Profiling - profilng of both Chula and apps running on it
#. Support for MySQL_ based session.  Currently only PostgreSQL_ and
   CouchDB are supported.  With either backend Memcached_ will continue to be
   used.

Who's using it
++++++++++++++

I don't actually know of anyone that's using it.  If you're using it,
let me know.

.. Internal hyperlinks
.. _About: about.html
.. _`Getting Started`: getting_started.html

.. External hyperlinks
.. _Apache: http://www.apache.org
.. _Cheetah: http://www.cheetahtemplate.org
.. _CouchDB: http://couchdb.apache.org
.. _couchdb-python: http://code.google.com/p/couchdb-python/
.. _FastCGI: http://en.wikipedia.org/wiki/FastCGI
.. _Flup: http://trac.saddi.com/flup
.. _Git: http://www.git.cz
.. _Github: http://www.github.com/jmcfarlane/chula
.. _Mako: http://www.makotemplates.org
.. _Memcached: http://www.memcached.org
.. _Mod_python: http://www.modpython.org
.. _Mod_WSGI: http://code.google.com/p/modwsgi/
.. _MVC: http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller
.. _MySQL: http://www.mysql.org
.. _Nginx: http://nginx.org
.. _package: http://docs.python.org/tutorial/modules.html#packages
.. _PostgreSQL: http://www.postgresql.org
.. _Psycopg2: https://dndg.it/cgi-bin/gitweb.cgi?p=public/psycopg2.git
.. _Python: http://www.python.org
.. _reST: http://www.restructuredtext.org
