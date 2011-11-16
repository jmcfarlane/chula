.. _downloads:

=========
Changelog
=========

..
 Chula v0.9.0 (dev)
 ++++++++++++++++++

 *Still under development*

 :Source: http://github.com/jmcfarlane/chula

Chula v0.13.0 (dev)
+++++++++++++++++++

*Released 2011-11-15*

- Add support for using the Eventlet wsgi provider.
- Add max-request, keep-alive, preload, worker-provider, and
  access-log support to :command:`chula-run`.
- Switch to httplib2 when running bat tests.
- Fix various http GET/POST bugs.

:Source: http://github.com/jmcfarlane/chula

Chula v0.12.0 (latest)
++++++++++++++++++++++

*Released 2011-08-02*

- Add support for using the Gunicorn wsgi provider.
- Add support for using the Tornado wsgi provider.
- Add support for "restfull" urls.  This feature is only available
  when using the regex mapper, see: :ref:`configuration`.
- Don't include a stacktrace for 404 requests served by
  :meth:`chula.www.controller.error.Error._crappy_static_server`.

:Documentation: `Chula-0.12.0 </0.12.0/>`_
:Download: `</downloads/Chula-0.12.0.tar.gz>`_
:Download: `</downloads/Chula-0.12.0.checksums>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.12.0

Chula v0.11.0 (stable)
++++++++++++++++++++++

*Released 2011-07-11*

- Improved setup to use distribute's setuptools, or distutils.
- Added (previously removed) support for python-2.5.

:Documentation: `Chula-0.11.0 </0.11.0/>`_
:Download: `</downloads/Chula-0.11.0.tar.gz>`_
:Download: `</downloads/Chula-0.11.0.checksums>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.11.0

Chula v0.10.0
+++++++++++++

*Released 2011-06-16*

- Fixed **major** defect in the http status header sent by
  :mod:`chula.www.adapters.fcgi.adapter` and
  :mod:`chula.www.adapters.wsgi.adapter`.  Prior to this fix it
  appears the status code would look something like ``404 OK`` in the
  event of a not found error condition.  The code had ``OK`` hard
  coded, and thus wasn't taking into consideration the actual status.
  This is now fixed using :attr:`httplib.responses` for the W3C string
  representations of the status code(s).
- Set psycopg2.extensions.{UNICODE,UNICODEARRAY} globally in
  :mod:`chula.db.engines.postgresql`.  This considerably simplifies
  unicode struggles when downstream code doesn't know what encoding
  was used.  With this change all data returned by psycopg2 will be of
  type :class:`unicode` instead of :class:`str`.
- Switched the :attr:`chula.config.Config.auto_reload` logic to fully
  reload everything.  Previously there were situations where
  code imported by model classes was not getting reloaded.  **This is
  currently experimental, and might eat your computer**.
- Improved :meth:`chula.www.controller.error.Error._crappy_static_server`
  so it can serve almost any static content (hypothetically).  For
  sure it can serve html files, which was sadly not supported
  previously.
- Improved :command:`chula-run` to use Gevent's wsgi server
  (http://www.gevent.org/gevent.wsgi.html) when available.  If not
  available the builtin :mod:`wsgiref.simple_server` is used.
- Added a default :class:`chula.logger.Logger` instance to
  :class:`chula.www.controller.base.Controller`.
- Added logging for 404 failures when
  :meth:`chula.www.controller.error.Error._crappy_static_server` is in
  use.
- Added logging for unhandled excpetions in controller methods
  decorated as a webservice, via :func:`chula.webservice.expose`.
- Added a :meth:`chula.www.controller.error.Error.e404_render` method
  to the base error controller for custom rendering while still using
  :meth:`chula.www.controller.error.Error._crappy_static_server` for
  testing.
- Added a skeleton application for use as a reasonable starting
  place for a hello world type application
  (https://github.com/jmcfarlane/chula/tree/master/apps/skel).

:Documentation: `Chula-0.10.0 </0.10.0/>`_
:Download: `</downloads/Chula-0.10.0.tar.gz>`_
:Download: `</downloads/Chula-0.10.0.checksums>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.10.0

Chula v0.9.0
++++++++++++

*Released 2011-03-24*

- Added :program:`chula-run` to serve a Chula application using
  Python's reference :mod:`wsgiref.simple_server`.  Remember this is
  just for debugging and developing.  When running your application
  for real you'll want to use something like :ref:`nginx_fastcgi`.
- [`GH-19 <http://github.com/jmcfarlane/chula/issues#issue/19>`_]
  Added :mod:`chula.www.controller.error` as a default error
  controller.  This provides basic static content handling as well as
  [crude] stack trace formatting in html when debugging is enabled.
- Added support for :attr:`chula.config.Config.auto_reload` to make coding
  even funner.
- Removed dependency on setuptools, now we only use :mod:`distutils`.
- [`GH-16 <http://github.com/jmcfarlane/chula/issues#issue/16>`_]
  Improved logging.  Both error and debug logging use files.  This
  fixes the long standing stderr blocking issue.
- Improved build process to reference build artifacts directly from
  pypi.
- [`GH-20 <http://github.com/jmcfarlane/chula/issues#issue/20>`_]
  Fixed :class:`chula.nosql.couch.Documents` to use ``document=value``.

:Documentation: `Chula-0.9.0 </0.9.0/>`_
:Download: `</downloads/Chula-0.9.0.tar.gz>`_
:Download: `</downloads/Chula-0.9.0.checksums>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.9.0

Chula v0.8.0
++++++++++++

*Released 2010-12-26*

* Added support for couchdb-python-0.7.0 (api changes).
* Added support for raw (json/xml) http posts
  (`GH-17 <http://github.com/jmcfarlane/chula/issues#issue/17>`_).
* Added support for the Python provided json library (now the default).
* Added support for "zero config" CouchDB access.  Previously the code
  would raise an excception of the server url was not specified, now
  it assumes http://localhost:5984 if no configuration is provided.
* Added support for optional webservice indentation when using the
  JSON transport.  This is useful for situations where you prefer to
  have payload you can actually read, and are ok with the performance
  impact.
* Exposed :attr:`chula.config.Config.log_level` in the config object.
* Improved `nosql.couch` class constructors to avoid kwargs overflow
  (`GH-18 <http://github.com/jmcfarlane/chula/issues#issue/18>`_).
* Improved the :doc:`getting_started` documentation a bit.
* Improved name of queue msg purging exception to be more accurate.
* Removed old xml based changelog and doc files.
* Removed support for Python-2.5 (though you can still use it).

:Documentation: `Chula-0.8.0 </0.8.0/>`_
:Download: `</downloads/Chula-0.8.0-py2.6.egg>`_
:Download: `</downloads/Chula-0.8.0-py3.1.egg>`_
:Download: `</downloads/Chula-0.8.0.tar.gz>`_
:Download: `</downloads/Chula-0.8.0-py2.6.linux-x86_64.exe>`_ (unsupported)
:Download: `</downloads/Chula-0.8.0.checksums>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.8.0

Older releases
++++++++++++++

Chula v0.7.0
^^^^^^^^^^^^

*Released 2010-06-29*

* Added support for native CouchDB sorting
* Removed support for app level sorting of CouchDB documents

:Documentation: `Chula-0.7.0 </0.7.0/>`_
:Download: `</downloads/Chula-0.7.0-py2.6.egg>`_
:Download: `</downloads/Chula-0.7.0-py2.5.egg>`_
:Download: `</downloads/Chula-0.7.0.tar.gz>`_
:Download: `</downloads/Chula-0.7.0-py2.6.linux-x86_64.exe>`_ (unsupported)
:Download: `</downloads/Chula-0.7.0-py2.5.win32.exe>`_ (unsupported)
:Download: `</downloads/Chula-0.7.0.checksums>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.7.0

Chula v0.6.0
^^^^^^^^^^^^

*Released 2010-05-07*

* Updated the manifest to include apps, and test cases
* Added support for Google App Engine.
* Added ability to fetch data from CouchDB using views
* Removed dependency on pytz.
* Removed usage of :func:`socket.gethostname`, which can have a
  negative impact on performance (especially in heavily threaded
  applications).  This also makes it possible to use Chula in
  environments that do not have access to :mod:`socket`.
* When looking for :mod:`simplejson`, also try using the copy that
  ships with Django.
* Updated the logger to not use a file handler when
  :attr:`chula.config.Config.log` is ``None``.
* Fixed defect in Couchdb connection cache.
* Performance improvements to :mod:`nosql.couch`

:Documentation: `Chula-0.6.0 </0.6.0/>`_
:Download: `</downloads/Chula-0.6.0-py2.6.egg>`_
:Download: `</downloads/Chula-0.6.0-py2.5.egg>`_
:Download: `</downloads/Chula-0.6.0.tar.gz>`_
:Download: `</downloads/Chula-0.6.0-py2.6.linux-x86_64.exe>`_ (unsupported)
:Download: `</downloads/Chula-0.6.0-py2.5.win32.exe>`_ (unsupported)
:Download: `</downloads/Chula-0.6.0.checksums>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.6.0

Chula v0.5.0
^^^^^^^^^^^^

*Released 2010-02-22*

* Added support for Setuptools.  This results in Chula being
  installable via ``easy_install``.
* Added a bit more documentation on how to install Chula.

:Documentation: `Chula-0.5.0 </0.5.0/>`_
:Download: `</downloads/Chula-0.5.0-py2.6.egg>`_
:Download: `</downloads/Chula-0.5.0-py2.5.egg>`_
:Download: `</downloads/Chula-0.5.0.tar.gz>`_
:Download: `</downloads/Chula-0.5.0-py2.6.linux-x86_64.exe>`_ (unsupported)
:Download: `</downloads/Chula-0.5.0-py2.5.win32.exe>`_ (unsupported)
:Download: `</downloads/Chula-0.5.0.checksums>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.5.0

Chula v0.4.0
^^^^^^^^^^^^

*Released 2010-02-10*

* Added simple wrapper around couchdb-python
* Added support for CouchDB session store. This means you now can
  choose between PostgreSQL/Memcached or CouchDB/Memcached.
* Added singleton decorator
* Added initial logging support
* Added a regex style url mapper. This means you can now choose
  between automatic class mapping and hand crafted mappings via regular
  expressions (this should be similar to Django style routing).
* Added (initial) documentation using Sphinx (not yet published)
* Updated memcache.py to version 1.45
* Fixed regression in chula.www.cookie where the cookie domain was
  getting prefixed with "." once for every cookie - oops.
* Refactored session into a package. When the CouchDB backend was
  added, not all of the failover logic was being implemented. To clean
  things up properly the session logic had to be abstracted away from
  the backends. Now there is a single session class that supports n
  number of backends that all use the same interface.
* Moved third party libs (fcgi, selenium, memcache) into chula.vendor

:Download: `Chula-0.4.0.tar.gz </downloads/Chula-0.4.0.tar.gz>`_
:Documentation: `Chula-0.4.0 </0.4.0/>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.4.0

Chula v0.3.0
^^^^^^^^^^^^

*Released 11/03/2009*

* Improved cookie handling (better RFC compliance)
* worked around Python-2.6 deprecation of Exception.message
* More unit and bat tests
* Enforced str key types with memcached
* Disabled memcached key sanitization by default

:Download: `Chula-0.3.0.tar.gz </downloads/Chula-0.3.0.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.3.0

Chula v0.2.0
^^^^^^^^^^^^

*Released 09/27/2009*

* Added chula.data.str2unicode
* Added initial bat tests
* Improved handling of exceptions during controller import
* Improved chula.mail to properly handle unicode
* Moved unit tests out of the source tree
* Added support for Selenium tests

:Download: `Chula-0.2.0.tar.gz </downloads/Chula-0.2.0.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.2.0

Chula v0.1.0
^^^^^^^^^^^^

*Released 06/29/2009*

* Fixed corner case in FieldStorage array structures
* Fixed defect in chula.date.str2date() with UTC +n
* Fixed run_tests so it works without Chula being installed
* Improved chula.data.str2date to support years 1000 to 2999 (jmathai).
* Improved chula.data.str2date to support a unix timetamp
* Added two sample applications
* Added documentation (one of the sample apps)
* Added support for custom queue messages
* Minor tweaks to reduce memory consumption
* Made session optional, but enabled by default

:Download: `Chula-0.1.0.tar.gz </downloads/Chula-0.1.0.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.1.0

Chula v0.0.6
^^^^^^^^^^^^

*Released 04/11/2009*

* Added support for FasgCGI
* Added an ASCII transport to chula.webservice
* Added a webservice decorator: chula.webservice.expose
* Added testutils module
* Fixed defect where error controller not found when using controller packages
* Fixed defect in data.commaify with less than 2 decimals
* Improved the timer to not break xhtml compliance

:Download: `Chula-0.0.6.tar.gz </downloads/Chula-0.0.6.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.0.6

Chula v0.0.5
^^^^^^^^^^^^

*Released 12/11/2008*

* Improved chula.collection adding an add() method
* Improved chula.webservice removing dependency on mod_python
* Improved chula.www.cookie removing dependency on mod_python
* Improved env to hold GET, POST (previously only a combo)
* Improved support for copy.deepcopy on chula.collection
* Improved error.e404 used when method resolution fails
* Improved "under construction" flow by removing dependency on session
* Improved chula.queue to keep processed/failed messages for later review
* Changed behavior to always call the error controller on exception.
  This is slightly less convienent, but encourages better testing of
  error handling code paths for apps using Chula.
* Changed behavior to call e404 when the controller requested isn't found
* Added initial support for WSGI
* Added initial suport for the Python simple_server

:Download: `Chula-0.0.5.tar.gz </downloads/Chula-0.0.5.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.0.5

Chula v0.0.4
^^^^^^^^^^^^

*Released 8/19/2008*

* Changed dependency checking to be further down the stack
* Cleaned up directory structure of source tree a little
* Improved installer to use distro specific locations
* Promoted chula.collection into a package
* Promoted chula.db into a package (much better now)
* Fixed defect in chula.collection when copy.deepcopy is used
* Wired up specified error controller (previously unused)
* Added chula.collection.UboundCollection
* Added chula.data.isregex and chula.db.cregex
* Added chula.mail
* Added chula.system
* Added support for an "under construction" controller
* Added support for sqlite to chula.db.datastore
* Added tcp based message queue (working, but very much not ready to be used)

:Download: `Chula-0.0.4.tar.gz </downloads/Chula-0.0.4.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.0.4

Chula v0.0.3
^^^^^^^^^^^^

*Released 6/15/2008*

* Added module for working with caching services, currently only
  Memcache is supported.
* Added support for controllers inside of packages, previously only a
  single namespace was supported.  Note that this feature is probably
  going to be moved into a FileMapper so the StandardMapper can move to
  more of a map based model.
* Added render method to pager.Pager for those that want to subclass the
  output. The base method simply returns the pager unmodified.
* Remove "danger" logic from db.py as it's best left up to the
  consumer to handle that type of logic. It was poorly implemented
  anyway :)

:Download: `Chula-0.0.3.tar.gz </downloads/Chula-0.0.3.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.0.3

Chula v0.0.2
^^^^^^^^^^^^

*Released 1/21/2008*

* Fixed defect where env.host is None
* Fixed defect where env.protocol_type is None
* Fixed defect where request_uri of: "/?" was loading e404
* Fixed defect where session not deleted on logout
* More gracefully handle clients lacking cookie support
* Allow the controller to have direct access to the cookie object.
  This provides access to it's destroy() method, useful for logout
  pages.
* Tweaks to improve support for static content
* Improved reliability/accuracy of session
* Added timer to html output (turn off with
  :attr:`chula.config.Config.add_timer`)
* Handle exception on premature client disconnection

:Download: `Chula-0.0.2.tar.gz </downloads/Chula-0.0.2.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.0.2

Chula v0.0.1
^^^^^^^^^^^^

*Released 12/14/2007*

* Initial release

:Download: `Chula-0.0.1.tar.gz </downloads/Chula-0.0.1.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.0.1
