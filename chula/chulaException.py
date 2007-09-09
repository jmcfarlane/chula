"""
Chula custom exceptions
"""

class BaseException(Exception):
    def __init__(self, msg=None):
        self.message = msg

    def __str__(self):
        if self.message is None:
            self.message = self.msg()
        return repr(self.message)

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
