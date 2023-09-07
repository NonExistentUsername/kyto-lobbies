import abc
import domain


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def get_game(self, id: str) -> domain.Game:
        game = self._get_game(id)
        if game:
            self.seen.add(game)
        return game

    def get_room(self, id: str) -> domain.Room:
        room = self._get_room(id)
        if room:
            self.seen.add(room)
        return room

    def get_player(self, id: str) -> domain.Player:
        player = self._get_player(id)
        if player:
            self.seen.add(player)
        return player

    @abc.abstractmethod
    def _get_game(self, id: str) -> domain.Game:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_room(self, id: str) -> domain.Room:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_player(self, id: str) -> domain.Player:
        raise NotImplementedError
