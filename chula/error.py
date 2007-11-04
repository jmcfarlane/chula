"""
Custom chula exceptions
"""

class BaseException(Exception):
    """
    Chula exception class which adds additional functionality to aid
    in efficiently raising custom exceptions.
    """

    def __init__(self, msg=None, append=None):
        """
        Create custom exception

        @param msg: Default exception message
        @type msg: String
        @param append: Message to be appended to the exception message
        @type append: String
        """

        self.message = msg
        self.append = append

    def __str__(self, append=None):
        """
        Return the message itself

        @param append: Additional info to be added to the message
        @type append: String
        @return: String
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

class ControllerClassNotFoundError(BaseException):
    """
    Exception indicating the requested controller class not found.
    """

    def __init__(self, _pkg, append=None):
        self.message = 'Unable to find the following class: %s' % _pkg
        self.append = append

class ControllerMethodNotFoundError(BaseException):
    """
    Exception indicating the requested controller method not found.
    """

    def __init__(self, _pkg, append=None):
        self.message = 'Unable to find the following method: %s' % _pkg
        self.append = append

class ControllerModuleNotFoundError(BaseException):
    """
    Exception indicating the requested module method not found.
    """

    def __init__(self, _pkg, append=None):
        self.message = 'Unable to find the following module: %s' % _pkg
        self.append = append

class ControllerMethodReturnError(BaseException):
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

class ExtremeDangerError(BaseException):
    """
    Exception indicating a refusal to do something dangerous.  Usually
    if this exception is raised you'll be glad it saved you from doing
    something stupid.
    """

    def msg(self):
        return 'Chula is not willing to perform the requested task'

class InvalidCollectionKeyError(BaseException):
    """
    Exception indicating an invalid key was used against a restricted
    collection class.
    """
    def __init__(self, key, append=None):
        self.message = 'Invalid key: %s' % key
        self.append = append

class MalformedConnectionStringError(BaseException):
    """
    Exception indicating that the database connection string used is
    invalid.
    """

    def msg(self):
        return 'Invalid database connection string'

class MalformedPasswordError(BaseException):
    """
    Exception indicating that the password used does not meet minimum
    requirements (aka: isn't strong enough).
    """

    def msg(self):
        return 'Password does not adhere to: chula.regex.PASSWD'

class TypeConversionError(BaseException):
    """
    Exception indicating that the requested data type conversion was
    not possible.
    """

    def __init__(self, _value, _type, append=None):
        self.message = 'Unable to convert value [%s] to type [%s]' \
            % (str(_value), str(_type))
        self.append = append

class UnsupportedUsageError(BaseException):
    """
    Exception indicating the chula api is being misused.
    """

    def msg(self):
        return 'Invalid use of this object'

class MissingDependancyError(BaseException):
    """
    Exception indicating a required dependancy of chula is either
    missing or of an incompatible version.
    """
    
    def __init__(self, _pkg, append=None):
        self.message = 'Please install: %s' % _pkg
        self.append = append

class RestrictecCollectionKeyRemovalError(BaseException):
    """
    It is illegal to remove a key from a RestrictedCollection object.
    """

    def __init__(self, key, append=None):
        self.message = ('Keys cannot be deleted from a'
                        'ResctrictedCollection object: %s' % key)
        self.append = append

class RestrictecCollectionMissingDefaultAttrError(BaseException):
    """
    Exception indicating that a restricted attribute was not given a
    default value.
    """

    def __init__(self, key, append=None):
        self.message = ('RestrictedCollection attribute missing'
                        'default value: %s' % key)
        self.append = append
