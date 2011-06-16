:mod:`chula.config` -- Configuration
====================================

.. index::
   single: config
   single: configuration
   pair: application; configuration

.. module:: chula.config

Chula applications read all configurations from a configuration file.
This file holds a :class:`Config` object.  Here's an example
configuration file::

 # Python imports
 import os

 # Third party imports
 from chula import config

 app = config.Config()
 app.classpath = 'controller'
 app.debug = True
 app.htdocs = os.path.join(os.path.dirname(__file__), '..', 'www')
 app.session = False

Of the configuration options above, the only one that you need to
understand now is: :attr:`Config.classpath`.

..
  :attr:`Config.error_controller` options.

.. class:: Config()

   This class provides an organized structure to hold all supported
   chula configuration options.  This class inherits from
   :class:`collection.restricted.RestrictedCollection`

   .. note::

      The following attributes are **mandatory**, meaning your
      configuration must provide values for them.

   .. attribute:: classpath

      The :attr:`classpath` option specifies a package in Python's
      path that holds one or more Chula controllers.  The convention
      typically used is ``controller``, which would be located in
      :file:`webapp/controller` from a fileystem perspective.  You can
      use any location you like, it just needs to be a valid Python
      package in Python's path.

      Most applications will either be installed or use a symlink expose the
      package without actually installing it.  Another option that's handy
      for development is to alter ``sys.path`` and inject the classpath at
      runtime.  This is really easy for standalone type apps - but might be
      able to do this with Mod_python_ and Mod_WSGI_ too.  The important
      thing here is that you need to have code that bootstraps Chula (so you
      can have a way to alter ``sys.path`` before Chula gets to it.

      There are two controllers that are special in that Chula needs to know
      exactly where they without any mapping logic.  These controllers also
      must have a few methods implemented.  The location of these
      controllers are relative to the defined :attr:`classpath`.

   .. note::

      The following attributes are all optional.

   .. attribute:: add_timer

      If :attr:`add_timer` is ``True`` an HTML fragment will be added to the
      body of the page, including the following pieces of information:

      * Chula adapter being used
      * Server hostname
      * Chula version
      * Processing time (server side)

      The fragment will look something like this::

       <div style="display:none;">
         <div id="CHULA_ADAPTER">FCGI/WSGI</div>
         <div id="CHULA_SERVER">li83-242</div>
         <div id="CHULA_VERSION">0.5.0</div>
         <div id="CHULA_COST">104.279995 ms</div>
       </div>

      This information can be used by client side javascript to display how
      fast search results were obtained, for example.  If your application
      happens to use aggressive caching (like full html caching) the timer
      will still be accurate.

      Default: ``True``

   .. attribute:: auto_reload

      If :attr:`auto_reload` is ``True`` Chula will try to reload the
      application with every http request.  The idea here is to save
      code in your editor, and refresh the browser - super handy.

      Default: ``False``

   .. attribute:: construction_controller

      The :attr:`construction_controller` specifies the controller to
      be called in the event the application is marked "under
      construction".  This is optional, but you'll be glad it's there
      when you need it.  The basic idea of the construction controller
      is that all requests get routed to it when a specific file
      exists on disk.  This means that when you need to take your site
      down for maintenance or something you can just *touch* the file
      configured via :attr:`construction_trigger`.

      The mandatory method that must exist in this controller is
      ``index()``.  For example with the above configuration this would be
      ``controller.construction.Construction.index()``.

   .. attribute:: construction_trigger

      Fully qualified path to a file on disk.  If the file exists, the
      construction controller will be called for all requests.

   .. attribute:: debug

      The :attr:`debug` flag has a default value of ``True`` and is
      only used by the Chula queue server.  It's main intention is
      really to be a hook that your application can use to alter it's
      behavior during development.

   .. attribute:: error_controller

      The :attr:`error_controller` specifies the controller to be
      called when something goes wrong.  Here are a few example use
      cases that will result in the error controller being called, and
      the corresponding method called:

      ============= ===========================================================
      Method        Use case
      ============= ===========================================================
      :meth:`e404`  The inbound request does not map to a controller.
      :meth:`e500`  During the processing of a request, and unhandled exception
                    is thrown within the controller.
      ============= ===========================================================

      Using an example configuration, if a request is made that cannot
      be mapped, Chula will call ``error.Error.e404()``.  If an
      unhandled exception occurs ``error.Error.e500()`` will be
      called.  This also means that if a request is made that cannot
      be mapped, and something goes wrong inside :meth:`e404` then
      both controller methods will actually get called.  This makes it
      very important that your error controller not be capable of
      throwing unhandled exceptions.

      If you want to have informative error pages during development,
      you'll want to place that code inside your error controller's
      :meth:`e500` method that exposes this information.  You can find a
      very simple implementation that does this inside this
      application's error controller and view.

      Default: :mod:`chula.www.controller.error`

   .. attribute:: htdocs

      Fully qualified path to a directory on disk.  When using the
      default :mod:`chula.www.controller.error` controller will serve
      static resources (css, js, html, png) from this directory.

      Default: ``None``

   .. attribute:: local

      The Chula configuration class is
      :class:`collection.restricted.RestrictedCollection`, meaning
      it's a dictionary with a pre defined set of keys.  Any key
      additions or removals will result in an exception.  This is done
      to ensure that the configuration is extremely stable.  In the
      event you would like to store configutation local to your
      application, the :attr:`local` attribute is available.  This can
      hold anything of your choosing.

   .. attribute:: log

      Fully qualified path to a file on disk.  This will will hold
      Chula specific logging.  The data sent to this file will only be
      warnings and above by default.  The default value is
      :file:`/tmp/chula.log`.  The user running the application must
      have write access to this file.

   .. attribute:: log_level

      This value is of type ``int`` and holds the threshold at which
      loging should occur.  The default value is ``logging.WARNING``.
      This means you will see warnings and errors, but not debug
      output.  If you change the value to ``logging.DEBUG`` you will
      get even more verbose output.  There is logic builtin to perform
      an offset for stdout logging.  So if you have
      :attr:`config.Config.debug` set to ``True`` the stdout logging
      will be more verbose than the file based logging.  Thus with the
      default configuration you get warnings and errors logged via the
      file, and debug and above via stdout.

   .. attribute:: mapper

      Chula currently has support for classpath and regex based url
      mappings.  The default value is to perform automatic classpath
      based mappings.

      **Classpath Mapper**

      The classpath mapper uses an algorithm to choose the right controller
      method for a given url.  Here are a few examples of the mapping
      algorithm used (assuming the configuration example at the top of this
      page):

      * http://localhost

        1. ``controller.home.Home.index()``

        With no :const:`env.REQUEST_URI` a direct call to the home
        controller can be made.  The home controller is named ``home``
        and is expected to be at the root of the specified
        :attr:`config.Config.classpath`, with a class named ``Home``
        and a method named ``index()``.

      * http://localhost/products

        1. ``controller.products.Products.index()``
        #. ``controller.home.Home.products()``
        #. ``controller.error.Error.e404()``

        When there is a single part this can either be a specified
        controller (and an assumed method) or this could be a specified
        method on the home controller.

      * http://localhost/products/dog

        1. ``controller.products.Products.Dog()``
        #. ``controller.error.Error.e404()``

        When there are two parts, it must be a specified controller and
        method.

      * http://localhost/products/dog/small

        1. ``controller.products.dog.Dog.index()``
        #. ``controller.error.Error.e404()``

        When there are more than two parts, it must be fully qualified,
        meaning a package(s), module, and controller.

      **Regex Mapper**

      In the event you would like to use regex style mappings, set this
      value to a tuple of dictionaries containing the regex:controller
      mappings.  Here is an example regex mapper::

       mapper = (
           (r'^$', 'home.index'),
           (r'^/about/?$', 'home.about'),
           (r'^/login/?$', 'auth.login'),
           (r'^/logout/?$', 'auth.logout')
       )

      In the map above, the first argument is a regular expression
      (this might actually become a compiled regex in time) that
      matches against :const:`env.REQUEST_URI`, and the second argument is a
      dot syntax that matches the relative path to a controller
      method.  The syntax assumes the path is all lower case, but it
      will expect all actual controller classes to have an upper cased
      first letter, and the parens on the method are implied.  So
      using the last map in the map above, the actual class/method
      used would be: ``controller.auth.Auth.logout()``

   .. attribute: mqueue_db

      Fully qualified path to a directory on disk.  When the Chula
      queue is used, this directory will be used to hold queue data.
      The default value is :file:`/tmp/chula/mqueue`.  The user running
      the queue must have write access to the directory.

   .. attribute:: mqueue_host

      Hostname that the Chula queue client and server should use.  The
      default value is ``localhost``.

   .. attribute:: session

      if :attr:`session` is ``True`` session is enabled, else not.
      Session is enabled by default.  See session_ for additional
      detail on setup and configuration.

   .. attribute:: session_db

      Database name used for persisting session.  The default value is
      ``chula_session``.

   .. attribute:: session_encryption_key

      I think this is a value no longer being used.  At one point the
      cookie value was being hashed.  Currently Chula is directly
      using :class:`Cookie.SimpleCookie` and at some point lost support for
      hashing the value.  This might be added back in at some point.

   .. attribute:: session_host

      Database host used for persisting session (currently only PostgreSQL)

   .. attribute:: session_max_stale_count

      The maximum number of session requests allowed to be served
      directly from the cache.  The default value for this setting is
      ``10``.  When the number of reqeusts exceed this value, the
      configured backend will be used.  This is designed to increase
      the scalability of the session store.  Chula session is always
      fronted by Memcached, and it's assumed that Memcached is
      reasonably reliable, thus with the default configuration the
      session backend will only see 10% of the traffic.  In the event
      of a cache miss, the backend is always used.  The only value in
      decreasing this value is to reduce the changes of stale data in
      the event of a cache failure.

   .. attribute:: session_memcache

      Memcached cluser to be used for session.  This value holds a list of
      tuples - each containing a hostname:port syntax. The default value is
      ``[('localhost:11211', 1)]``.  This value is directly fed to
      memcache.py which happens to be bundled with Chula.

      NOTE: There are plans to add support for libmemcached_

   .. attribute:: session_name

      The name of the the session cookie to be sent to the browser.  The
      default value is ``chula-session``.

   .. attribute:: session_nosql

      HTTP path to a running CouchDB_ installation.  If this value is
      specified, CouchDB will be used for the session backend instead of
      PostgreSQL.  The default value is ``None`` - which means PostgreSQL_ is
      currently the default backend session store.

   .. attribute:: session_password

      Password to the PostgreSQL session database

   .. attribute:: session_port

      Port to the PostgreSQL session database

   .. attribute:: session_timeout

      Session timeout value

   .. attribute:: session_username

      Username to the PostgreSQL session database

   .. attribute:: strict_method_resolution

      If :attr:`strict_method_resolution` is ``True`` the url mapper
      will send the request directly to the error controller (:meth:`e404`
      method) if a direct map is not possible.  So basically the
      mappers will not attempt to use the implied ``index()`` method.
      This is not true for the homepage, as it's always an implied map
      to ``home.index()``.  The default value is ``False``.

.. _session: session.html

.. _FastCGI: http://en.wikipedia.org/wiki/FastCGI
.. _Memcached: http://www.memcached.org
.. _Mod_python: http://www.modpython.org
.. _Mod_WSGI: http://code.google.com/p/modwsgi/
.. _MySQL: http://www.mysql.org
.. _PostgreSQL: http://www.postgresql.org
.. _libmemcached:  http://code.google.com/p/python-libmemcached/
.. _CouchDB: http://couchdb.apache.org
