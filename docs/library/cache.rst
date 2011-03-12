:mod:`chula.cache` -- Wrapper module for upstream memcache.py
=============================================================

.. index::
   single: caching
   single: wrapper
   pair: upstream; wrapper
   pair: wrapper; upstream
   pair: caching; objects

.. module:: cache

.. data:: ENCODING

   Encoding to be used with memcache keys.  Default value is ``ASCII``

.. data:: SANITIZE

   Should invalid characters in the key be removed.  Default is ``False``

.. class:: Cache(servers)

   Takes a list of two element tuples representing a memcached cluster

   .. staticmethod:: clean_key(key, sanitize=SANITIZE)

      Return a valid key encoded via :const:`ENCODING`.  Sanitization
      of illegal caracters from the key will be performed if
      *sanitize* is ``True``.  If the key is too long, or *sanitize*
      is ``False`` and illegal characters are found in the key, an
      :class:`error.InvalidCacheKeyError` exception will be raised.

   .. method:: close()

      Close client connection to server.

   .. method:: delete(key)

      Delete *key* from the cluster, returning ``True`` if deleted,
      ``False`` if not.

   .. method:: get(key)

      Fetch the value in memcache associated with *key*.

   .. method:: purge(key)

      Alias for :meth:`delete`.

   .. method:: set(key, value)

      Set *value* in the memcache cluster using *key*.  Returns
      ``True`` if successfully persisted, else returns ``False``.

   .. method:: stats()

      Return a ``list`` of stats per server.
