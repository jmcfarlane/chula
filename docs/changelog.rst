=======================
Downloads/Release Notes
=======================

Chula v0.4.0 (dev)
++++++++++++++++++

*Not yet released*

* Added simple wrapper around couchdb-python
* Added support for couchdb session store. This means you now can
  choose between PostgreSQL/Memcached or CouchDB/Memcached.
* Added singleton decorator
* Added initial logging support
* Added a regex style url mapper. This means you can now choose
  between automatic class mapping and hand crafted mappings via regular
  expressions (this should be similar to Django style routing).
* Updated memcache.py to version 1.45
* Fixed regression in chula.www.cookie where the cookie domain was
  getting prefixed with "." once for every cookie - oops.
* Refactored session into a package. When the couchdb backend was
  added, not all of the failover logic was being implemented. To clean
  things up properly the session logic had to be abstracted away from
  the backends. Now there is a single session class that supports n
  number of backends that all use the same interface.

.. :Download: `Chula-0.4.0 </downloads/Chula-0.4.0.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula

Chula v0.3.0
++++++++++++

*Released 11/03/2009*

* Improved cookie handling (better RFC compliance)
* worked around Python-2.6 deprecation of Exception.message
* More unit and bat tests
* Enforced str key types with memcached
* Disabled memcached key sanitization by default

:Download: `Chula-0.3.0 </downloads/Chula-0.3.0.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.3.0

Chula v0.2.0
++++++++++++

*Released 09/27/2009*

* Added chula.data.str2unicode
* Added initial bat tests
* Improved handling of exceptions during controller import
* Improved chula.mail to properly handle unicode
* Moved unit tests out of the source tree
* Added support for Selenium tests

:Download: `Chula-0.2.0 </downloads/Chula-0.2.0.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.2.0

Chula v0.1.0
++++++++++++

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

:Download: `Chula-0.1.0 </downloads/Chula-0.1.0.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.1.0

Chula v0.0.6
++++++++++++

*Released 04/11/2009*

* Added support for FasgCGI
* Added an ASCII transport to chula.webservice
* Added a webservice decorator: chula.webservice.expose
* Added testutils module
* Fixed defect where error controller not found when using controller packages
* Fixed defect in data.commaify with less than 2 decimals
* Improved the timer to not break xhtml compliance

:Download: `Chula-0.0.6 </downloads/Chula-0.0.6.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.0.6

Chula v0.0.5
++++++++++++

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

:Download: `Chula-0.0.5 </downloads/Chula-0.0.5.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.0.5

Chula v0.0.4
++++++++++++

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

:Download: `Chula-0.0.4 </downloads/Chula-0.0.4.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.0.4

Chula v0.0.3
++++++++++++

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

:Download: `Chula-0.0.3 </downloads/Chula-0.0.3.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.0.3

Chula v0.0.2
++++++++++++

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
* Added timer to html output (turn off with config.add_timer)
* Handle exception on premature client disconnection

:Download: `Chula-0.0.2 </downloads/Chula-0.0.2.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.0.2

Chula v0.0.1
++++++++++++

*Released 12/14/2007*

* Initial release

:Download: `Chula-0.0.1 </downloads/Chula-0.0.1.tar.gz>`_
:Source: http://github.com/jmcfarlane/chula/tree/v0.0.1
