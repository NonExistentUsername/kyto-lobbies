class Player:
    def __init__(self, id: str):
        self.__id = id

    @property
    def id(self) -> str:
        """
        Getter for id

        Returns:
            str: id
        """
        return self.__id
