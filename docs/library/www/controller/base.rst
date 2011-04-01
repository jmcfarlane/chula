:mod:`chula.www.controller.base` -- Base controller
===================================================

.. index::
   single: controller

.. automodule:: chula.www.controller.base

   .. autoclass:: Controller
      :members:

      .. automethod:: __init__
      .. automethod:: _gc
      .. automethod:: _pre_session_persist

Useful attributes
+++++++++++++++++

.. attribute:: content_type

   Attribute holding the
   :attr:`chula.www.adapters.env.BaseEnv.content_type`.
   Mutating this value will determine the outgoing HTTP
   ``Content-Type``.

   Here's how you would set the content type inside a
   controller:

   >>> from chula import json
   >>> from chula.www.controller import base
   >>>
   >>> class Foo(base.Controller):
   ...     def bar(self):
   ...         self.content_type = 'application/json'
   ...         payload = {'testing':'hello world'}
   ...         return json.dumps(payload, indent=2)
   >>>

.. attribute:: config

   Attribute holding the :class:`chula.config.Config` object.

.. attribute:: env

   Attribute holding the :class:`chula.www.adapters.env.BaseEnv` object.

   Example of how to reference GET variables:

   >>> from chula.www.controller import base
   >>>
   >>> class Foo(base.Controller):
   ...     def http_get_variables(self):
   ...         html = []
   ...         html.append('<ul>')
   ...         for key, value in self.env.form_get.iteritems():
   ...             html.append('<li>%s = %s</li>' % (key, value))
   ...         html.append('</ul>')
   ...         return ''.join(html)
   >>>

   Example of how to reference POST variables:

   >>> from chula.www.controller import base
   >>>
   >>> class Foo(base.Controller):
   ...     def http_get_variables(self):
   ...         html = []
   ...         html.append('<ul>')
   ...         for key, value in self.env.form_post.iteritems():
   ...             html.append('<li>%s = %s</li>' % (key, value))
   ...         html.append('</ul>')
   ...         return ''.join(html)
   >>>

   Example of how to reference raw HTTP POST data:

   >>> from chula.www.controller import base
   >>>
   >>> class Foo(base.Controller):
   ...     def http_get_variables(self):
   ...         return self.env.form_raw
   >>>

.. attribute:: form

   Attribute referencing :attr:`chula.www.adapters.env.BaseEnv.form`.
   Rember this attribute is just a pointer to the combined form
   attribute, if you need more control reference one of the
   ``form_foo`` attributes in
   :attr:`chula.www.adapters.env.BaseEnv.form`.

   Example of how to reference form variables:

   >>> from chula.www.controller import base
   >>>
   >>> class Foo(base.Controller):
   ...     def form_variables(self):
   ...         html = []
   ...         html.append('<ul>')
   ...         for key, value in self.form.iteritems():
   ...             html.append('<li>%s = %s</li>' % (key, value))
   ...         html.append('</ul>')
   ...         return ''.join(html)
   >>>

.. attribute:: log

   Attribute holding :class:`chula.logger.Logger` object.  The
   intended use of this attribute is to allow app specific logging.
   The default configuration will send ``error`` messags to
   :attr:`chula.config.Config.log` and debug messages (and higher) to
   :attr:`chula.config.Config.log` suffixed with ``.debug``

.. attribute:: model

   Attribute holding :class:`chula.collection.Collection`
   object.  The intended use of this attribute is to populate
   with data, and pass it to the view.

.. attribute:: session

   Attribute holding an instance of
   :class:`chula.session.Session` object.

   .. note::

      This attribute only exists if
      :attr:`chula.config.Config.session` is ``True``

   .. note::

      This attribute is also automatically exposed to the model
      attribute.

