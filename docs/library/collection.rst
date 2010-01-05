:mod:`collection`
=================

.. index::
   single: collection

.. data:: collection.UNSET

   :class:`collection.base.Base` key who's value has not yet been set by the
   consumer.

:class:`Base`
+++++++++++++

.. module:: collection.base
.. class:: Base()

   Flexible collection that supports both dictionary and attribute
   style access.

:class:`Restricted`
+++++++++++++++++++

.. module:: collection.restricted
.. class:: RestrictedCollection()

   Collection with constrained keys.  This means that every instance
   of this class is guaranteed to **only** have the keys defined in
   the class.  Removal of any of it's keys raise an
   :class:`error.RestrictecCollectionKeyRemovalError`, and any key
   additions will result in :class:`error.InvalidCollectionKeyError`
   being raised.  Though the keys in this class are guarenteed, their
   values can either be defaulted, or set by the consumer.  The
   setting of the keys by the consumer is enforced by an
   :class:`error.RestrictecCollectionMissingDefaultAttrError`
   exception being raised if :const:`collection.UNSET`.
   
   This class inherits from :class:`collection.base.Base`.
