class PychexException(Exception):
    """ All other exceptions inherit from PychexException """
    pass


class PychexSecurityImageMismatchError(PychexException):
    """ Raised when the security image returned from Paychex is incorrect """
    pass


class PychexSecurityImageMissingError(PychexException):
    """ Raised when we try to login before getting the security image """
    pass


class PychexInvalidPasswordError(PychexException):
    """ Raised when an invalid password is used at any point in the flow """
    pass


class PychexUnauthenticatedError(PychexException):
    """
    Raised when we try to make requests that require authentication before we
    have authenticated
    """
    pass


class PychexNoBolUsernameError(PychexException):
    """
    Raised when we try to log in to Benefits OnLine before obtaining the
    username
    """
    pass


class PychexUnknownError(PychexException):
    """ Raised when we have an unknown error, such as HTTP 500 """
    pass
