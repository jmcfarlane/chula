=====================
Optional dependencies
=====================

Chula doesn't have any dependencies unless you use session.  If you
want support for session, you will use one of the following:

Postgresql
++++++++++

Install the server and client::

 sudo apt-get intall postgresql python-psycopg2

Then download the source Chula tarball from :ref:`downloads` and do::

 tar -zxvf path/to/downloaded/tarball
 sudo su - postgres
 cd /path/to/exploded/tarball
 ./sql/session/rebuild

This will create a user, database, and schema.

CouchDB
++++++++++

Install the server and client::

 sudo apt-get intall couchdb python-couchdb
