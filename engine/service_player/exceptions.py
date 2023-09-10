class InternalException(Exception):
    pass


class PlayerAlreadyExists(InternalException):
    pass


class InvalidPlayerUsername(InternalException):
    pass
