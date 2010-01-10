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

 cd wherever_you_unpacked_the_chula_tarball
 ./apps/basic/webserver

At this point you should be able to point your browser at
http://localhost:8080 and browse a hello world application that ships
with Chula.  The actual purpose of the application is to serve as a
way to run BAT_ tests, but it's useful for this purpose as well.

Hit :kbd:`Control-c` to stop the server, and let's move on.

Create your own hello world application
+++++++++++++++++++++++++++++++++++++++

Directory structure
~~~~~~~~~~~~~~~~~~~

The structure we want so far will support view templates, web server
configuration, client side static files, and a python package::

 cd Desktop
 mkdir -p Myapp/config    # Web server configs
 mkdir -p Myapp/myapp     # Python package
 mkdir -p Myapp/view      # View emplates
 mkdir -p Myapp/www       # Static files (client side)

Make ``myapp`` an actual python package::

 touch Myapp/myapp/__init__.py

Configuration
~~~~~~~~~~~~~

Create the following file in :file:`Myapp/myapp/configuration.py`::
 
 from chula import config
 
 # Development configuration
 dev = config.Config()
 dev.classpath = 'myapp.controllers'
 dev.construction_controller = 'error'
 dev.construction_trigger = '/tmp/myapp.stop'
 dev.debug = True
 dev.error_controller = 'error'
 dev.session = False

Controllers
~~~~~~~~~~~

Create a package called ``controllers`` to hold all app controllers,
this makes it easy to distinguish controllers from your other python
modules you might have::
 
 mkdir Myapp/myapp/controllers
 touch Myapp/myapp/controllers/__init__.py

Create the **mandatory** ``error`` controller configured previously by creating :file:`Myapp/myapp/controllers/error.py` ::

 from chula.www import controller

 class Error(controller.Controller):
     def index(self):
         return 'Sorry, the site is down for maintenance'
 
     def e404(self):
         return 'Page not found'
 
     def e500(self):
         return 'Trapped Error: %s' % self.model.exception.exception

Now create a controller that will serve as the homepage, as well as a
blog or something, :file:`Myapp/myapp/controllers/home.py` ::

 from chula.www import controller

 class Home(controller.Controller):
     def index(self):
         return 'Hello world'
 
     def blog(self):
         return 'This is my blog'

At this point we have a full Chula application, but we don't have a
way to run it.  For now, let's create a standalone web server script
for testing purposes.  Next, we'll actually wire up the application
against a few different web servers.

Test server
~~~~~~~~~~~

Create :file:`Myapp/webserver.py` ::

 import os
 import sys
 from wsgiref.simple_server import make_server

 from chula.www.adapters.wsgi import adapter
 
 # Expose the myapp python package, as it's not "installed"
 sys.path.insert(0, os.getcwd())
 
 # Import my configuration we created above
 from myapp import configuration
 
 # Define a wsgi application, passing in our (dev) configuration
 @adapter.wsgi
 def application():
     return configuration.dev
 
 # Setup a simple server using the proxy app and it's configuration
 port = 8080
 httpd = make_server('', port, application)
 try:
     print 'Starting server on: http://localhost:%s' % port
     httpd.serve_forever()
 except KeyboardInterrupt:
     sys.exit() 

Test it!
~~~~~~~~

Let's try out what we have so far::

 cd Myapp
 python webserver.py

At this point you should be able to browse the following urls:

#. http://localhost:8080
#. http://localhost:8080/blog

Hit :kbd:`Control-c` to stop the server.

Add env vars
~~~~~~~~~~~~

Let's add a page that's a little bit more usefull.  This one will
generate an HTML table of the environment variables.  This page will
also use Mako_ for the view.

Update controller
^^^^^^^^^^^^^^^^^

Let's update our ``home`` controller
to look like this, :file:`Myapp/myapp/controllers/home.py` ::

 from chula.www import controller

 # This is a new import
 from mako.template import Template

 class Home(controller.Controller):
     def index(self):
         return 'Hello world'
 
     def blog(self):
         return 'This is my blog'

     # This is the new method
     def envinfo(self):
         # Add env variables to the model
         self.model.env = self.env

         # Load our Mako template
         view = Template(filename='view/envinfo.tmpl')

         # Return the rendered template, passing in our model
         return view.render(model=self.model)

Mako template
^^^^^^^^^^^^^

Now let's create the mako template referenced above,
:file:`Myapp/view/envinfo.tmpl` ::

 <html>
 <head><title>Env Variables</title></head>
 <body>
   <h1>Environment Variables</h1>
   <table>
     <tr>
       <th>Key</th>
       <th>Value</th>
     </tr>
     %for key, value in model.env.iteritems():
       <tr>
         <td valign="top">${key}</td>
         <td>${value}</td>
       </tr>
     %endfor
   </table>
 </body>
 </html>

Try it!
^^^^^^^

Let's see what this looks like now::

 cd Myapp
 python webserver.py

Now browse to http://localhost:8080/envinfo and you should see a table
of environment variables.  It's a little hard to read because the keys
are not sorted, but that's because keys in the standard dict are not
sorted.  I leave the sorting issue as an excercise for the reader :)

Hit :kbd:`Control-c` to stop the server.

Web server integration
+++++++++++++++++++++++

Chula integrates with WSGI_, Mod_python_, and FastCGI_.  Let's go
thru how you would integrate your hello world application with each of
these.

Nginx via FastCGI
~~~~~~~~~~~~~~~~~

Todo

Apache via Mod_python
~~~~~~~~~~~~~~~~~~~~~

Todo

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
