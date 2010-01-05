:mod:`error` -- Chula exceptions
================================

.. index::
   single: exceptions
   single: errors
   pair: exception; handling

.. module:: error

.. class:: ChulaException(msg=None, append=None)

   Chula exception class which adds additional functionality to aid in
   efficiently raising custom exceptions.

   .. method:: _get_message()

      Getter for a message property, to avoid using an attribute named
      "message" which will raise deprecation errors in Python-2.6.
      Returns self._message

   .. method:: _set_message(msg)

      Getter for a message property, to avoid using an attribute
      named "message" which will raise deprecation errors in
      Python-2.6.

   .. method:: __str__(append=None)

      Return the message itself

   .. method:: msg()

      When the msg method is not overloaded, return a generic
      message

.. class:: ControllerClassNotFoundError(_pkg, append=None)

   Exception indicating the requested controller class not found.
   Inherits from :class:`ChulaException`

.. class:: ControllerImportError(_pkg, append=None)

    Exception while trying to import the controller.  Inherits from
    :class:`ChulaException`

.. class:: ControllerMethodNotFoundError(_pkg, append=None)

    Exception indicating the requested controller method not found.
    Inherits from :class:`ChulaException`

.. class:: ControllerModuleNotFoundError(_pkg, append=None)

    Exception indicating the requested module method not found.
    Inherits from :class:`ChulaException`

.. class:: ControllerMethodReturnError()

    Exception indicating that a controller method is returning
    ``None``, which is probably not on purpose.  It's true that we do
    cast all output as a string, thus 'None' is technically valid, it's
    most likely that the controller method simply forgot to return.
    This will save time by pointing this out.  If you really need to
    return ``None``, then return: 'None'.  Inherits from
    :class:`ChulaException`

.. class:: ControllerRedirectionError()

    Exception indicating that the controller was unable to perform the
    requested redirect.  Inherits from :class:`ChulaException`

.. class:: InvalidAttributeError(key, append=None)

    Exception indicating an invalid attribute was used.  Inherits from
    :class:`ChulaException`

.. class:: InvalidCacheKeyError(key, append=None)

    Exception indicating an invalid key was used against a cache
    source.  Inherits from :class:`ChulaException`

.. class:: InvalidCollectionKeyError(key, append=None)

    Exception indicating an invalid key was used against a restricted
    collection class.  Inherits from :class:`ChulaException`

.. class:: MalformedConnectionStringError()

    Exception indicating that the database connection string used is
    invalid.  Inherits from :class:`ChulaException`

.. class:: MalformedPasswordError()

    Exception indicating that the password used does not meet minimum
    requirements (aka: isn't strong enough).  Inherits from
    :class:`ChulaException`

.. class:: TypeConversionError(_value, _type, append=None)

    Exception indicating that the requested data type conversion was
    not possible.  Inherits from :class:`ChulaException`

.. class:: UnsupportedDatabaseEngineError(engine, append=None)

    Exception indicating a requst for an unsupported database engine
    Inherits from :class:`ChulaException`

.. class:: UnsupportedMapperError(_pkg, append=None)

    Exception indicating an invalid mapper configuration Inherits from
    :class:`ChulaException`
    
.. class:: UnsupportedUsageError()

    Exception indicating the chula api is being misused.  Inherits
    from :class:`ChulaException`

.. class:: MissingDependencyError(_pkg, append=None)

    Exception indicating a required dependency of chula is either
    missing or of an incompatible version.  Inherits from
    :class:`ChulaException`

.. class:: RestrictecCollectionKeyRemovalError(key, append=None)

    It is illegal to remove a key from a RestrictedCollection object.
    Inherits from :class:`ChulaException`

.. class:: RestrictecCollectionMissingDefaultAttrError(key, append=None)

    Exception indicating that a restricted attribute was not given a
    default value.  Inherits from :class:`ChulaException`

.. class:: SessionUnableToPersistError()

    Chula is unable to persist either to PostgreSQL or Memached.
    Inherits from :class:`ChulaException`

.. class:: WebserviceUnknownTransportError(key, append=None)

    Exception indicating that the specified webservice transport is
    either unknown or unsupported.  Inherits from
    :class:`ChulaException`
