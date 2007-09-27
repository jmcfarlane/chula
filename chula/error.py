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

class ControllerMethodNotFoundError(BaseException):
    """
    Exception indicating the requested controller method not found.
    """

    def __init__(self, _pkg, append=None):
        self.message = 'Please create a working %s method' % _pkg
        self.append = append

class ExtremeDangerError(BaseException):
    """
    Exception indicating a refusal to do something dangerous.  Usually
    if this exception is raised you'll be glad it saved you from doing
    something stupid.
    """

    def msg(self):
        return 'Chula is not willing to perform the requested task'

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

class UnsupportedConfigError(BaseException):
    """
    Exception indicating the use of an unsupported chula configuration
    attribute.  See chula.config for the supported attributes.
    """

    def msg(self):
        return 'The specified configuration attribute is unsupported'

class MissingDependancyError(BaseException):
    """
    Exception indicating a required dependancy of chula is either
    missing or of an incompatible version.
    """
    
    def __init__(self, _pkg, append=None):
        self.message = 'Please install: %s' % _pkg
        self.append = append

