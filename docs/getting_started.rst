===============
Getting Started
===============

.. toctree::
   :maxdepth: 2

   install

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

 |-- model
 |   |-- configuration.py
 |   `-- __init__.py
 |-- view
 |   |-- error.tmpl
 |   `-- home.tmpl
 |-- controller
 |   |-- error.py
 |   |-- home.py
 |   `-- __init__.py
 |-- www
 |   |-- jquery.js
 |   `-- style.css
 `-- webserver.py

In the list of files above you can see the model, view, controller,
and static web resources (www).  The webserver is not specific to
Chula really, but rather a quick and dirty way to launch a Chula
application without needing a webserver installed and configured.
Technically speaking this is all you need to run a Chula application.

Run a sample Chula application
++++++++++++++++++++++++++++++

If you would like to try the above application right now, you'd type
this in your terminal::

 cd wherever_you_unpacked_the_chula_tarball
 python apps/example/webapp/webserver.py

At this point you should be able to point your browser at
http://localhost:8080 and browse a hello world application that ships
with Chula.  The actual purpose of the application is to serve as a
way to run BAT_ tests, but it's useful for this purpose as well.

Hit :kbd:`Control-c` to stop the server, and let's move on.

Create your own hello world application
+++++++++++++++++++++++++++++++++++++++

Directory structure
~~~~~~~~~~~~~~~~~~~

The structure we want is a typical MVC_ web application deployed
against a typical web server::

 cd Desktop
 mkdir -p myapp/config      # Web server configs
 mkdir -p myapp/model       # Model
 mkdir -p myapp/view        # View
 mkdir -p myapp/controller  # Controller
 mkdir -p myapp/www         # Static files

Make the ``model`` and ``controller`` actual python packages::

 touch myapp/model/__init__.py
 touch myapp/controller/__init__.py

Configuration
~~~~~~~~~~~~~

Create the following file in :file:`myapp/model/configuration.py`::
 
 from chula import config
 
 # Development configuration
 app = config.Config()
 app.classpath = 'controller'
 app.construction_controller = 'error'
 app.construction_trigger = '/tmp/myapp.stop'
 app.debug = True
 app.error_controller = 'error'
 app.session = False

 app.mapper = (
   (r'^/myapp/?$', 'home.index'),
   (r'^/myapp/home/?$', 'home.index'),
   (r'^/myapp/blog/?$', 'home.blog'),
   (r'^/myapp/envinfo/?$', 'home.envinfo'),
 )

Controllers
~~~~~~~~~~~

Create the **mandatory** ``error`` controller configured previously by
creating :file:`myapp/controller/error.py` ::

 from chula.www import controller

 class Error(controller.Controller):
     def index(self):
         return 'Sorry, the site is down for maintenance'
 
     def e404(self):
         return 'Page not found'
 
     def e500(self):
         return 'Trapped Error: %s' % self.model.exception.exception

Now create a controller that will serve as the homepage, as well as a
blog or something, :file:`myapp/controller/home.py` ::

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

Create :file:`myapp/webserver.py`::

 import os
 import sys
 from wsgiref.simple_server import make_server

 from chula.www.adapters.wsgi import adapter
 
 # Expose the myapp, as it's not "installed"
 sys.path.insert(0, os.getcwd())
 
 # Import my configuration we created above
 from model import configuration
 
 # Define a wsgi application, passing in our (dev) configuration
 @adapter.wsgi
 def application():
     return configuration.app
 
 def main():
     # Setup a simple server using the proxy app and it's configuration
     port = 8080
     httpd = make_server('', port, application)
     try:
         print 'Starting server on: http://localhost:%s' % port
         httpd.serve_forever()
     except KeyboardInterrupt:
         sys.exit() 

 if __name__ == '__main__':
     main()

Test it!
~~~~~~~~

Let's try out what we have so far::

 python myapp/webserver.py

At this point you should be able to browse the following urls:

#. http://localhost:8080/myapp
#. http://localhost:8080/myapp/blog

Hit :kbd:`Control-c` to stop the server.

Add env vars
~~~~~~~~~~~~

Let's add a page that's a little bit more usefull.  This one will
generate an HTML table of the environment variables.  This page will
also use Mako_ for the view.

Update controller
^^^^^^^^^^^^^^^^^

Let's update our ``home`` controller
to look like this, :file:`myapp/controller/home.py` ::

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
:file:`myapp/view/envinfo.tmpl` ::

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

 python myapp/webserver.py

Now browse to http://localhost:8080/myapp/envinfo and you should see a table
of environment variables.  It's a little hard to read because the keys
are not sorted, but that's because keys in the standard dict are not
sorted.  I leave the sorting issue as an excercise for the reader :)

Hit :kbd:`Control-c` to stop the server.

Web server integration
++++++++++++++++++++++

Chula integrates with WSGI_, Mod_python_, and FastCGI_.  Let's go
thru how you would integrate your hello world application with each of
these.

.. toctree::
   :maxdepth: 1

   nginx
   mod_wsgi
   mod_python

What's next
+++++++++++

When creating your own application is's going to be important that you
understand the configuration options available.  You'll also want to
learn more about featues available, and how to use them.  You can find
detail on configuration `here <library/config.html>`_.

.. _Apache: http://www.apache.org
.. _BAT: http://en.wikipedia.org/wiki/Acceptance_testing
.. _Cheetah: http://www.cheetahtemplate.org
.. _FastCGI: http://en.wikipedia.org/wiki/FastCGI
.. _Mako: http://www.makotemplates.org
.. _Mod_python: http://www.modpython.org
.. _Mod_WSGI: http://code.google.com/p/modwsgi/
.. _MVC: http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller
.. _Nginx: http://nginx.org
.. _package: http://docs.python.org/tutorial/modules.html#packages
.. _reST: http://www.restructuredtext.org
.. _WsGI: http://www.wsgi.org
