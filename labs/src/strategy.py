from __future__ import annotations
from .move import Move
from .nim import Nim
from dataclasses import dataclass
from typing import Callable
from random import choice, randint
from copy import deepcopy

def analize(raw: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = dict()
    for ply in (Move(r, o) for r, c in enumerate(raw.rows) for o in range(1, c + 1)):
        tmp: Nim = deepcopy(raw)
        tmp.nimming(ply)
        cooked["possible_moves"][ply] = tmp.nim_sum()
    return cooked

def optimal(game_state: Nim) -> Move:
    analysis = analize(game_state)
    # logging.debug(f"analysis:\n{pformat(analysis)}")
    spicy_moves = [ply for ply, ns in analysis["possible_moves"].items() if ns != 0]
    if not spicy_moves:
        spicy_moves = list(analysis["possible_moves"].keys())
    ply = choice(spicy_moves)
    return ply

def pure_random(game_state: Nim) -> Move:
    """A completely random move"""
    row = choice([r for r, c in enumerate(game_state.rows) if c > 0])
    num_objects = randint(1, game_state.rows[row])
    return Move(row, num_objects)

def gabriele(game_state: Nim) -> Move:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(game_state.rows) for o in range(1, c + 1)]
    return Move(*max(possible_moves, key=lambda m: (-m[0], m[1])))

def expert_system(state: Nim) -> Move:
    current_nim_sum = state.nim_sum()
    stable_state = current_nim_sum == 0
    remaining_rows = [row for row in state.rows if row > 0]
    if len(remaining_rows) == 2 and 1 in state.rows:
        largest_row = max(state.rows)
        largest_row_index = state.rows.index(largest_row)
        return Move(largest_row_index, largest_row)
    if stable_state:
        # you cannot leave a stable state, make a minimal move
        longest_row = max(state.rows)
        longest_row_index = state.rows.index(longest_row)
        return Move(longest_row_index, 1)
    # leave a stable state to the opponent
    for index, row in enumerate(state.rows):
        if row & current_nim_sum ^ current_nim_sum == 0:
            return Move(index, current_nim_sum)
    raise ValueError('Move not found')

@dataclass(frozen=True)
class Strategy():
    name: str
    move_maker: Callable[[Nim], Move]

    def make_move(self, game_state: Nim) -> Move:
        return self.move_maker(game_state)

    @classmethod
    def random(cls) -> Strategy:
        return cls('Random', pure_random)

    @classmethod
    def gabriele(cls) -> Strategy:
        return cls('Gabriele', gabriele)

    @classmethod
    def optimal(cls) -> Strategy:
        return cls('Optimal', optimal)

    @classmethod
    def expert_system(cls) -> Strategy:
        return cls('Expert system', expert_system)

    @staticmethod
    def all() -> list[Strategy]:
        return [Strategy.random(), Strategy.gabriele(), Strategy.optimal(), Strategy.expert_system()]