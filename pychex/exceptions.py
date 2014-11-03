class PychexException(Exception):
    pass


class PychexSecurityImageMismatchError(PychexException):
    pass


class PychexSecurityImageMissingError(PychexException):
    pass


class PychexInvalidPasswordError(PychexException):
    pass


class PychexUnauthenticatedError(PychexException):
    pass


class PychexNoAppUsernameError(PychexException):
    pass
