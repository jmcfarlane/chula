"""
Custom chula exceptions
"""

class ChulaException(Exception):
    """
    Chula exception class which adds additional functionality to aid
    in efficiently raising custom exceptions.
    """

    def __init__(self, msg=None, append=None):
        """
        Create custom exception

        :param msg: Default exception message
        :type msg: :class:`str`
        :param append: Message to be appended to the exception message
        :type append: :class:`str`
        """

        self._message = None
        self.append = append

    def _get_message(self):
        """
        Getter for a message property, to avoid using an attribute
        named "message" which will raise deprecation errors in
        Python-2.6.
        """

        return self._message

    def _set_message(self, msg):
        """
        Getter for a message property, to avoid using an attribute
        named "message" which will raise deprecation errors in
        Python-2.6.

        :param msg: Error message to be used
        :type msg: :class:`str`
        """

        self._message = msg

    message = property(_get_message, _set_message)

    def __str__(self, append=None):
        """
        Return the message itself

        :param append: Additional info to be added to the message
        :type append: :class:`str`
        :return: :class:`str
        """

        if self.message is None:
            self.message = self.msg()

        if self.append is None:
            return repr(self.message)
        else:
            return repr(self.message + ': ' + self.append)

    def msg(self):
        """
        When the msg method is not overloaded, return a generic
        message
        """

        return 'Generic chula exception'

class ControllerClassNotFoundError(ChulaException):
    """
    Exception indicating the requested controller class not found.
    """

    def __init__(self, _pkg, append=None):
        self.message = 'Unable to find the following class: %s' % _pkg
        self.append = append

class ControllerImportError(ChulaException):
    """
    Exception while trying to import the controller.
    """

    def __init__(self, _pkg, append=None):
        self.message = 'Error while trying to import: %s' % _pkg
        self.append = append

class ControllerMethodNotFoundError(ChulaException):
    """
    Exception indicating the requested controller method not found.
    """

    def __init__(self, _pkg, append=None):
        self.message = 'Unable to find the following method: %s' % _pkg
        self.append = append

class ControllerModuleNotFoundError(ChulaException):
    """
    Exception indicating the requested module method not found.
    """

    def __init__(self, _pkg, append=None):
        self.message = 'Unable to find the following module: %s' % _pkg
        self.append = append

class ControllerMethodReturnError(ChulaException):
    """
    Exception indicating that a controller method is returning None,
    which is probably not on purpose.  It's true that we do cast all
    output as a string, thus None is technically valid, it's most
    likely that the controller method simply forgot to return.  This
    will save time by pointing this out.  If you really need to return
    None, then return: 'None'
    """

    def msg(self):
        return "Method either didn't return, or returned None"

class ControllerRedirectionError(ChulaException):
    """
    Exception indicating that the controller was unable to perform the
    requested redirect.
    """

    def msg(self):
        return "Unable to redirect as requested"

class InvalidAttributeError(ChulaException):
    """
    Exception indicating an invalid attribute was used.
    """
    def __init__(self, key, append=None):
        self.message = 'Invalid attribute: %s' % key
        self.append = append

class InvalidCacheKeyError(ChulaException):
    """
    Exception indicating an invalid key was used against a cache source.
    """
    def __init__(self, key, append=None):
        self.message = 'Invalid key: %s' % key
        self.append = append

class InvalidCollectionKeyError(ChulaException):
    """
    Exception indicating an invalid key was used against a restricted
    collection class.
    """
    def __init__(self, key, append=None):
        self.message = 'Invalid key: %s' % key
        self.append = append

class MalformedConnectionStringError(ChulaException):
    """
    Exception indicating that the database connection string used is
    invalid.
    """

    def msg(self):
        return 'Invalid database connection string'

class MalformedPasswordError(ChulaException):
    """
    Exception indicating that the password used does not meet minimum
    requirements (aka: isn't strong enough).
    """

    def msg(self):
        return 'Password does not adhere to: chula.regex.PASSWD'

class TypeConversionError(ChulaException):
    """
    Exception indicating that the requested data type conversion was
    not possible.
    """

    def __init__(self, _value, _type, append=None):
        self.message = 'Unable to convert value [%s] to type [%s]' \
            % (str(_value), str(_type))
        self.append = append

class UnsupportedDatabaseEngineError(ChulaException):
    """
    Exception indicating a requst for an unsupported database engine
    """

    def __init__(self, engine, append=None):
        self.message = 'Unsupported db engine: %s' % engine
        self.append = append

class UnsupportedMapperError(ChulaException):
    """
    Exception indicating an invalid mapper configuration
    """

    def __init__(self, _pkg, append=None):
        self.message = 'Invalid chula.config.mapper class: %s' % _pkg
        self.append = append

class UnsupportedUsageError(ChulaException):
    """
    Exception indicating the chula api is being misused.
    """

    def msg(self):
        return 'Invalid use of this object'

class MissingDependencyError(ChulaException):
    """
    Exception indicating a required dependency of chula is either
    missing or of an incompatible version.
    """

    def __init__(self, _pkg, append=None):
        self.message = 'Please install: %s' % _pkg
        self.append = append

class RestrictecCollectionKeyRemovalError(ChulaException):
    """
    It is illegal to remove a key from a RestrictedCollection object.
    """

    def __init__(self, key, append=None):
        self.message = ('Keys cannot be deleted from a'
                        'ResctrictedCollection object: %s' % key)
        self.append = append

class RestrictecCollectionMissingDefaultAttrError(ChulaException):
    """
    Exception indicating that a restricted attribute was not given a
    default value.
    """

    def __init__(self, key, append=None):
        self.message = 'Please set the "%s" attr to fix this' % key
        self.append = append

class SessionUnableToPersistError(ChulaException):
    """
    Chula is unable to persist either to PostgreSQL or Memached.
    """

    def msg(self):
        return 'Unable to persist session, all backends failed'

class WebserviceUnknownTransportError(ChulaException):
    """
    Exception indicating that the specified webservice transport is
    either unknown or unsupported.
    """

    def __init__(self, key, append=None):
        self.message = 'Unknown transport: "%s"' % key
        self.append = append
