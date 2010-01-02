===========
About Chula
===========

History
+++++++

Chula is written by John McFarlane (aka me).  When I first wanted to learn
Python I started a project named *Apple*.  At the time there were lots
of frameworks for building web applications with Python, but I was
interested in learning Python so it seemed more fun to make my own.
Additionally I was surprised by the complexity of other frameworks.  I
was looking for something a bit simpler.

I hacked on Apple for a few years, and then decided to start over and
try to improve things based on what I had learned - 3 months later I
released the first version of Chula.  Since that time I've tried to
improve things and add features as needed, but I never lost sight of
it's main purpose: to be a vehicle for me to have fun and learn stuff.

If you're really wanting to build the next killer application I'd
prolly recommend using `Django <http://djangoproject.org>`__.  If
you're looing for something smaller or even just something *different*
then give Chula a try :)

Features
++++++++

 * Web servers: Most of the common setups are supported (Mod_Python_,
   Mod_WSGI_, and FastCGI_).
 * Session: Uses both Memcached_ and PostgreSQL_ for cluster safe
   storage that scales pretty well.
 * Message queue: Support for asynchronous processing of messages
 * Typical stuff: Environment, GET and POST variables
 * Speed: Chula seems to perform pretty well

Source code
+++++++++++

Chula uses the Git_ version control system.  The official Chula repository
can be found on Github_.

Issue tracker
+++++++++++++

Chula uses the issue tracker that's integrated with Github_.  If you
find defects or have ideas for improvement please feel free to file
issues.  In the event Chula becomes more popular, a more sophisticated
tracker will be used.

Release cycle
+++++++++++++

I generally try to release a new version around 4 times a year.

Roadmap
+++++++

The roadmap right now is pretty small.  Here are the features I'm
currently thinking about:

  1. Logging - This needs to happen sooner or later
  2. Implementing a regex based mapper (see: `Getting Started`_)
  3. Profiling - profilng of both Chula and apps running on it
  4. Support for MySQL_ based session.  Currently only PostgreSQL_ is
     supported.  With either backend Memcached_ will continue to be
     used.

Who's using it
++++++++++++++

I don't actually know of anyone that's using it.  If you're using it,
let me know.

.. include:: links.rst
