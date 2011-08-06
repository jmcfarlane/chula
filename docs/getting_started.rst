.. installation:

===============
Getting Started
===============

Preferred::

 sudo pip install chula

Alternatiely::

 sudo easy_install chula

.. toctree::
   :maxdepth: 2

   install

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
 `-- www
     |-- jquery.js
     `-- style.css

In the list of files above you can see the model, view, controller,
and static web resources (www).

Reference: MVC_

Create an app!
++++++++++++++

Create the directory structure::

 cd Desktop
 mkdir -p myapp/model       # Model
 mkdir -p myapp/view        # View
 mkdir -p myapp/controller  # Controller
 mkdir -p myapp/www         # Static files

Make the ``model`` and ``controller`` actual python packages::

 touch myapp/model/__init__.py
 touch myapp/controller/__init__.py

.. _configuration:

Configuration
^^^^^^^^^^^^^

Create the following file in :file:`myapp/model/configuration.py`::

 # Python imports
 import os

 # Third party imports
 from chula import config

 app = config.Config()
 app.classpath = 'controller'
 app.debug = True
 app.htdocs = os.path.join(os.path.dirname(__file__), '..', 'www')
 app.session = False

 app.mapper = (
   (r'^/myapp/?$', 'home.index'),
   (r'^/myapp/home/?$', 'home.index'),
   (r'^/myapp/blog/?$', 'home.blog'),
   (r'^/myapp/envinfo/?$', 'home.envinfo'),
 )

If you want to use restfull style urls you can use named capturing
groups (:mod:`re`) in your app mapper.  Consider::

 app.mapper = (
  (r'^/blog'                              # blog
    '(/(?P<username>[a-z]+))?'            # username
    '(/(?P<date>\d\d\d\d-\d\d-\d\d))?'    # date
    '(/(?P<commens>comments))?'           # comments
    '?/?$',                               # Optional trailing slash
   'rest.blog'),
 )

The above route would match: ``/blog/jmcfarlane/2010-05-12/comments``
and would expose username, date, and comments via
:attr:`chula.www.adapters.env.BaseEnv.form_rest`.

Controllers
^^^^^^^^^^^

Create a controller that will serve as the homepage, as well as a
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

Test it!
^^^^^^^^

Let's try out what we have so far::

 chula-run myapp

At this point you should be able to browse the following urls:

#. http://localhost:8080/myapp
#. http://localhost:8080/myapp/blog

Hit :kbd:`Control-c` to stop the server.

Add more to it
++++++++++++++

Let's add a page that's a little bit more usefull.  This one will
generate an HTML table of the environment variables.  This page will
also use Mako_ for the view.

Controller
^^^^^^^^^^

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

View
^^^^

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

 chula-run myapp

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

You can also run any Chula application with many of the existing WSGI
providers, such as:

- Python's builtin :mod:`SimpleHTTPServer`
- `Eventlet <http://www.eventlet.net>`_
- `Gevent <http://www.gevent.org>`_
- `Gunicorn <http://gunicorn.org>`_
- `Tornado <http://www.tornadoweb.org>`_

By default :program:`chula-run` will try to find and use whatever WSGI
provider is available, but you can specifically tell it which one to
use (if supported) via the :option:`-P` argument.  For example::

 # Gevent
 chula-run -P gevent myapp

 # Gunicorn
 chula-run -P gunicorn myapp

 # Eventlet
 chula-run -P eventlet myapp

 # Tornado
 chula-run -P tornado myapp

 # SimpleHTTPServer
 chula-run -P builtin myapp

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
