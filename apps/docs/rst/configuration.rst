===============================
Chula Application Configuration
===============================

.. include:: rst/lib/toc.rst

Introduction
++++++++++++

Chula applications read all configurations from a configuration file.
This file holds a ``chula.config.Config`` object.  Here's an example
configuration file::

  from chula import config

  prod = config.Config()
  prod.classpath = 'example.www.controllers'
  prod.construction_controller = 'construction'
  prod.construction_trigger = '/tmp/chula_example.stop'
  prod.debug = False
  prod.error_controller = 'error'
  prod.session = False

Of the configuration options above, the only two that you need to
understand now are the ``classpath``, ``error_controller`` and
``construction_controller`` options.

Classpath
---------

The ``classpath`` option specifies a package in Python's path that
holds Chula controllers.  The convention typically used is
``project.www.controllers``.  You can use any location you like, it
just needs to be a valid Python package.

Most applications will either be installed or use a symlink to pseudo
*install* it.  Another option that's handy for development is to alter
``sys.path`` and inject the classpath at runtime.  This is really easy
for standalone type apps - but might be able to do this with
Mod_python_ and Mod_WSGI_ too.  The important thing here is that you
need to have code that bootstraps Chula (so you can have a way to
alter ``sys.path`` before Chula gets to it.

Special controllers
-------------------

There are two controllers that are special in that Chula needs to know
exactly where they without any mapping logic.  These controllers also
must have a few methods implemented.  The location of these
controllers are relative to the defined ``classpath``.

Construction
~~~~~~~~~~~~

The ``construction_controller`` specifies the controller to be called
in the event the application is marked "under construction".  For now
this isn't super important - but it'll be glad it's there when you
need it.

The basic idea of the construction controller is that all requests get
routed to it when a specific file exists on disk.  This means that
when you need to take your site down for maintenance or something you
can just *touch* a file.

The mandatory method that must exist in this controller is
``index()``.  For example with the above configuration this would be
``example.www.controllers.construction.index()``.

Error
~~~~~

The ``error_controller`` specifies the controller to be called when
something goes wrong.  Here are a few example use cases that will
result in the error controller being called, and the corresponding
method called in it:
 
======= ====================================================================
Method  Use case
======= ====================================================================
e404    The inbound request does not map to a controller.  Currently the
        mapping happens via package structure as implemented in
        ``chula.www.maper.standard``.  In time there will be various
        types of mappers available.  Most likely the default one in
        time will be configuration based - meaning you will define
        regex patterns that determine where to route requests.
        
e500    The controller is the main class responsible for coordinating 
        everything.  The controller is responsible for capturing user
        input, calling the model for processing, invoking the view,
        passing the model to the view, and returning view to the
        client (usually a browser).
======= ====================================================================

Using the example configuration above, if a request is made that
cannot be mapped, Chula will call
``example.www.controllers.error.e404()``.  If you're unlucky enough to
have an unhandled exception, then
``example.www.controllers.error.e500()`` will be called.  This also
means that if a request is made that cannot be mapped, and something
then goes wrong inside ``e404()`` then both will actually get called.

If you want to have friendly error pages to view exceptions when in
development, you'll want to place that code inside your error
controller's ``e500`` method.  method.  You can look at this
application's error controller to get a feel for how might look with a
very simple implementation.

.. include:: rst/lib/links.rst
.. include:: rst/lib/extras.rst
