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


class RamRepository(AbstractRepository):
    def __init__(self, games: dict = None, rooms: dict = None, players: dict = None):
        super().__init__()
        self._games = {}
        self._rooms = {}
        self._players = {}

    def copy(self) -> "RamRepository":
        return RamRepository(
            self._games.copy(), self._rooms.copy(), self._players.copy()
        )

    def _get_game(self, id: str) -> domain.Game:
        return self._games.get(id)

    def _get_room(self, id: str) -> domain.Room:
        return self._rooms.get(id)

    def _get_player(self, id: str) -> domain.Player:
        return self._players.get(id)

    def add_game(self, game: domain.Game):
        self._games[game.id] = game

    def add_room(self, room: domain.Room):
        self._rooms[room.id] = room

    def add_player(self, player: domain.Player):
        self._players[player.id] = player
