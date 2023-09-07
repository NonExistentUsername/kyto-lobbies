from uuid import UUID


class Player:
    def __init__(self, id: UUID):
        self.__id = id

    @property
    def id(self) -> UUID:
        """
        Getter for id

        Returns:
            UUID: id
        """
        return self.__id
