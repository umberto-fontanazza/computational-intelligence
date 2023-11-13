from .nim import Nim
from .strategy import Strategy
from .move import Move
from logging import INFO, info, WARNING, basicConfig

class Game():

    def __init__(self, initial_rows: int, player: Strategy, opponent: Strategy, play_first: bool):
        self._nim = Nim(initial_rows)
        self._player = player
        self._opponent = opponent
        self._player_turn = play_first

    def __str__(self):
        return f'\t{self._nim} Turn: {'player' if self._player_turn else 'opponent'} '

    def play_turn(self):
        active_player = self._player if self._player_turn else self._opponent
        move: Move = active_player.make_move(self._nim)
        self._nim.nimming(move)
        self._player_turn = not self._player_turn

    def play(self, logging = False):
        if logging:
            basicConfig(level = INFO)
            info(f'\tLogging game {self._player} vs {self._opponent}')
            info(self)
        while not self._nim.game_over():
            self.play_turn()
            if logging:
                info(self)

    def player_wins(self) -> bool:
        self.play()
        return self._player_turn