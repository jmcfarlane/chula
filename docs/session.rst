=======
Session
=======

Chula includes session support via cookies and backend servers.
Currently there are three supported backends:

1. Memcached
2. PostgreSQL
3. CouchDB

Via configuration you can choose between PostgreSQL or CouchDB as the
main session store - Memcached is always used as a cache.

Cluster safe
++++++++++++

Because local storage is not used, Chula is has cluster safe session.
Basically this means that you can fire up multiple instances of your
application and they all share session.  This also means you don't
have to use `sticky sessions` in your load balancer configuration.

Scalable
++++++++

Chula maintains session in Memcached_ backed by a persistent data
store.  Because Memcache is reasonably reliable, only a percentage of
session requests are actually sent to the backend.  The default
configuration is to update the backend every 10 requests.  This means
the session backend (which is slower than cache) is only serving 10%
of the actual traffic.  The frequency of backend updates is
configurable via :attr:`config.Config.session_max_stale_count`, and
the backend is always consulted in the event of a cache miss.

A current limitation of the session store is that it does not use
connection pooling.  This can optionally be added by fronting your
PostgreSQL server with pgpool_.  When CouchDB is used as the backend,
connection pooling isn't relevent as it uses HTTP.

Native storage
++++++++++++++

Chula stores your session values as pickle_'d strings (via cPickle) thus
you can store any values that are serializeable by cPickle.

Maintenance
+++++++++++

Chula does not clean up all PostgreSQL based sessions.  You will
likely want to configure a cron job to periodically delete stale
sessions from the database.  When CouchDB is used, the sessions are
sharded by year/month.  This allows you to easily purge off old
sessions by year/month.

Setup
+++++

PostgreSQL
----------

In order to use Chula session you will need to create the database
used by the backend.  Use the following command to create them::

 user# sudo su - postgres  ## Or whatever user PostgreSQL is running as
 postgres# cd wherever_you_unpacked_the_chula_tarball
 postgres# ./sql/session/reload

The above command will create a user named ``chula`` and a database
named ``chula_session``.  Next you'll need to make sure your server is
configured to support requests over TCP/IP.  Usually this is done by
setting ``listen_addresses = 'localhost'`` or another hostname in
``postgresql.conf``.

Assuming you're connecting to the server running locally, you're all
done!

If you're connecting to a remote server, you need to add the hostname
in your configuration via :attr:`config.Config.session_host`.  If you
want to use a different user/password/port/server you are free to do
so.

CouchDB
-------

You wil need to configure :attr:`config.Config.session_nosql` with the
full HTTP path to your CouchDB server.  If this is a local install,
you'd set the value to http://localhost:5984.  Don't worry about the
database, as it wil be created automatically on demand.

Memcached
---------

You need to configure your cluster information via
:attr:`config.Config.session_memcache`.  If you're using a local
install of Memcached you can just take the defaults, else configure it
with something like this::

 [('host1:11211', 1), ('host2:11211', 1), ('host3:11211', 1)]

Reference
+++++++++

For more detail on Chula configuration in general, see
:mod:`config`.

.. _pgpool: http://pgpool.projects.postgresql.org/
.. _pickle: http://docs.python.org/library/pickle.html
