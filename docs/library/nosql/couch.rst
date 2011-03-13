:mod:`chula.nosql.couch` -- Wrapper for python-couchdb
======================================================

.. index::
   single: couch

.. automodule:: chula.nosql.couch

Document
++++++++

.. autoclass:: Document(id [, db_conn=None, document=None, server=None, shard=None, track_dirty=None])
   :members: __init__, delete, sanitize_id

Documents
+++++++++

.. autoclass:: Documents([, db_conn=None, document=None, server=None, shard=None, track_dirty=None])
   :members: __init__, query, view

Helper functions
++++++++++++++++

.. autofunction:: chula.nosql.couch.connect(db [, shard=None, server=None])
