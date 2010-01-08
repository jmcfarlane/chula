===============
Getting Started
===============

Terminology
+++++++++++

Welcome to Chula. Let's go thru a few things before you get started
building your first app.  Chula is a simple toolkit that is based on
the MVC_ pattern.  From now on we'll use the terms "*model*",
"*view*", and "*controller*" when describing things.  Here's a brief
summary of what these terms as they relate to Chula:

=========== ===================================================================
Term        Description
=========== ===================================================================
Model       The logic and data of an application.  These are usually
            standard Python classes.  They do work, implement
            algorithms, and hold data.

View        The view is responsible for presentation.  Examples of
            this would be:

            * Mako_
            * Cheetah_
            * reST_ (restructured text)

Controller  The controller is the main class responsible for coordinating 
            everything.  The controller is responsible for capturing
            user input, calling the model for processing, invoking the
            view, passing the model to the view, and returning
            view's output to the client.
=========== ===================================================================

Application structure
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

In the list of files above there is a Python package_ named ``example``
that holds the entire application.  Inside it there are two
controllers, a configuration, and a webserver.  The webserver is not
specific to Chula really, but rather a quick and dirty way to launch a
Chula application without needing a webserver installed and
configured.  Technically speaking this is all you need to run a Chula
application.

Run a sample Chula application
++++++++++++++++++++++++++++++

If you would like to try the above application right now, you'd type
this in your terminal::

 user# cd wherever_you_unpacked_the_chula_tarball
 user# ./apps/basic/webserver

At this point you should be able to point your browser at
http://localhost:8080 and browse a hello world application that ships
with Chula.  The actual purpose of the application is to serve as a
way to run BAT_ tests, but it's useful for this purpose as well.

Create your own hello world application
+++++++++++++++++++++++++++++++++++++++

Todo...

Web server integration
+++++++++++++++++++++++

Chula integrates with WSGI_, ,Mod_Python_, and FastCGI_.  Let's go
thru how you would integrate your hello world application with each of
these.

What's next
+++++++++++

When creating your own application is's going to be important that you
understand the configuration options available.  You'll also want to
learn more about featues available, and how to use them.  You can find
detail on configuration `here <library/config.html>`_.

.. _BAT: http://en.wikipedia.org/wiki/Acceptance_testing
.. _Cheetah: http://www.cheetahtemplate.org
.. _FastCGI: http://en.wikipedia.org/wiki/FastCGI
.. _Mako: http://www.makotemplates.org
.. _Mod_python: http://www.modpython.org
.. _MVC: http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller
.. _package: http://docs.python.org/tutorial/modules.html#packages
.. _reST: http://www.restructuredtext.org
.. _WsGI: http://www.wsgi.org