from nim import Nim
from strategy import Strategy
from move import Move

class Game():

    def __init__(self, initial_rows: int, player: Strategy, opponent: Strategy, play_first: bool):
        self._nim = Nim(initial_rows)
        self._player = player
        self._opponent = opponent
        self._player_turn = play_first

    def play_turn(self):
        active_player = self._player if self._player_turn else self._opponent
        move: Move = active_player.make_move(self._nim)
        self._nim.nimming(move)
        self._player_turn = not self._player_turn

    def player_wins(self) -> bool:
        while not self._nim.game_over():
            self.play_turn()
        return self._player_turn