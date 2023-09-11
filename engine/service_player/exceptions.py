class InternalException(Exception):
    pass


class PlayerAlreadyExists(InternalException):
    pass


class PlayerDoesNotExist(InternalException):
    pass


class InvalidPlayerUsername(InternalException):
    pass


class RoomAlreadyExists(InternalException):
    pass
