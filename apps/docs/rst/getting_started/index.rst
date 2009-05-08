===============
Getting Started
===============

.. include:: rst/lib/toc.rst

Terminology
+++++++++++

Welcome to Chula. Let's go thru a few things before you get started
building your first app.  Chula is a simple toolkit that is based on
the MVC_ pattern.  From now on we'll use the terms "*model*",
"*view*", and "*controller*" when describing things.  Here's a brief
summary of what these terms as they relate to Chula:

========== ====================================================================
Term        Description
========== ====================================================================
Model       The logic and data of an application.  These are usually
            standard Python classes.  They do work, implement
            algorithms, and hold data.
View        The view is responsible for presentation.  Examples of
            this would be:

            * Mako_
            * Cheetah_
Controller  The controller is the main code path that controlls
            everything.  The controller is responsible for capturing
            user input, calling the model for processing, invoking the
            template, and returning something to the browser.
========== ====================================================================

Application Structure
+++++++++++++++++++++

Here is an example file structure of a bare bones Chula application::

  |-- example
  |   |-- __init__.py
  |   |-- configuration.py
  |   `-- www
  |       |-- __init__.py
  |       `-- controllers
  |           |-- __init__.py
  |           |-- error.py
  |           `-- home.py
  `-- webserver

In the list of files there is a Python package_ named *example* that
holds the entire application.  Inside it there are two controllers, a
configuration, and a webserver.  The webserver is not specific
to Chula really, but rather a quick and dirty way to launch a Chula
application without needing a webserver installed and configured.
Technically speaking this is all you need to run a Chula application.
If you would like to try the above application right now, you'd type
this in your terminal::

  user# cd wherever_you_unpacked_the_chula_tarball
  user# cd apps/basic
  user# ./webserver

At this point you should be able to point your browser at
http://localhost:8080 and browse a really fancy Chula app :)

Configuration
+++++++++++++

Chula applications read all configurations from a configuration file
which holds a reference to a Chula *config* object.  Here's an example
configuration file::

  import copy

  from chula import config

  # Prod config
  prod = config.Config()
  prod.classpath = 'example.www.controllers'
  prod.construction_controller = 'construction'
  prod.construction_trigger = '/tmp/chula_example.stop'
  prod.debug = False
  prod.error_controller = 'error'
  prod.local.view_cache = None
  prod.session = False

Of the configuration options above, the only two that you need to
understand now are the ``classpath`` and ``construction_controller`` options.

Classpath
---------

The ``classpath`` option specifies which namespace in your code holds
the controllers.  The convention typicall used is
``project.www.controllers``.

Construction Controller
-----------------------

The ``construction_controller`` specifies the controller to be called
in the event the application is marked "under construction".  For now
this isn't super important - but it'll be handy when you need it.

.. include:: rst/lib/links.rst
.. include:: rst/lib/extras.rst
