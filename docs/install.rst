============
Installation
============

You can install Chula in various ways, depending on what type of
operating system you have, and how your system is configured.

Chula
+++++

Easy Install
^^^^^^^^^^^^

Probably the easiest way to install Chula is to use ``easy_install``.
If your system has Setuptools installed, you can simply do::

 sudo easy_install chula

If you do not have ``easy_install`` you can easily get it for Linux,
Mac, and windows from their website: http://pypi.python.org/pypi/setuptools.

Tarball
^^^^^^^

If you don't have Setuptools, or don't want to use ``easy_install`` for
whatever reason, you can download the latest source tarball from
:ref:`downloads` and do the following, where you would replace "a.b.c"
with "|version|" - you get the idea: ::

 tar -zxvf Chula-a.b.c.tar.gz
 cd Chula-a.b.c
 sudo python setup.py install

Windows
^^^^^^^

For you windows cats, you can use the two methods above, or you can
download the windows specific installer found here :ref:`downloads`.
Then just execute the installer, and follow the prompts.

Dependencies
++++++++++++

Mandatory
^^^^^^^^^

Currently the aren't any mandadory dependencies beyond Python itself,
so this will give you 5 minutes to go make a latte :)

Optional
^^^^^^^^

If you want support for session, you will use one of the following:

Postgresql
~~~~~~~~~~

Install the server and client::

 sudo apt-get intall postgresql python-psycopg2

Then download the source Chula tarball from :ref:`downloads` and do::

 tar -zxvf path/to/downloaded/tarball
 sudo su - postgres
 cd /path/to/exploded/tarball
 ./sql/session/rebuild

This will create a user, database, and schema.

CouchDB
~~~~~~~

Install the server and client::

 sudo apt-get intall couchdb python-couchdb


.. External hyperlinks
.. _Python: http://www.python.org
.. _reST: http://www.restructuredtext.org
.. _Simplejson: http://www.undefined.org/python/
