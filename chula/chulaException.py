"""
Chula custom exceptions
"""

class BaseException(Exception):
    def __init__(self, msg=None, append=''):
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
        if self.message is None:
            self.message = self.msg()

        if self.append != '':
            self.append = ': %s' % self.append

        return repr(self.message + self.append)

    def msg(self):
        return 'Generic chula exception'

class UnauthorizedOperationError(BaseException):
    def msg(self):
        return 'Unauthorized operation. See sub-exception for specific error.'

class IllegalOperationError(BaseException):
    def msg(self):
        return "Yeah... it doesn't really work like that."

class MalformedPasswordError(BaseException):
    def msg(self):
        return 'Password does not adhere to: chula.regex.PASSWD'

class UnsupportedUsageError(BaseException):
    def msg(self):
        return 'Invalid use of this object'

class UnsupportedSettingError(BaseException):
    def msg(self):
        return 'The specified attribute is unsupported'
