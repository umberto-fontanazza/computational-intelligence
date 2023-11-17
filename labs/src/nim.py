from __future__ import annotations
from typing import Callable
from .move import Move
from functools import reduce
from operator import xor
from numpy import array

def nim_sum_simplified(game_state: Nim) -> int:
    return reduce(xor, game_state.rows)

def nim_sum_original(game_state: Nim) -> int:
    tmp = array([tuple(int(x) for x in f"{c:032b}") for c in game_state.rows])
    xor = tmp.sum(axis=0) % 2
    return int("".join(str(_) for _ in xor), base=2)

class Nim:
    @staticmethod
    def from_rows(rows: list[int]):
        num_rows = len(rows)
        nim = Nim(num_rows)
        nim._rows = [row for row in rows]
        return nim

    def __init__(self, num_rows: int, k: int | None = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return not self.game_over()

    def __str__(self):
        return f'<{' '.join(str(row) for row in self._rows)}>\t{'stable' if self.nim_sum() == 0 else 'unstable'}'

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    def nimming(self, ply: Move) -> None:
        row, num_objects = ply.row, ply.quantity
        assert self._rows[row] >= num_objects
        assert ply.quantity > 0
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects

    def game_over(self):
        return sum(self._rows) == 0

    def nim_sum(self) -> int:
        nim_sum_function: Callable[..., int] = nim_sum_simplified # to be tested
        return nim_sum_function(self)