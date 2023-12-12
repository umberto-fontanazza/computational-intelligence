from __future__ import annotations
from typing import Literal, Callable
from dataclasses import dataclass
from itertools import product
from collections.abc import Iterable
from functools import cache

Action = tuple[int, int]
Quality = float
Symbol = Literal['O', 'X']
Row = tuple[Symbol, Symbol, Symbol]

@dataclass(frozen=True)
class State():
    board: tuple[Row, Row, Row]
    current_player: Literal['X', 'O']

    @property
    @cache
    def winner(self) -> Literal['X', 'O', '_']:
        """This method was written by https://bard.google.com/chat, and just tweaked by me on an attempt to test
        Google's Gemini released on december 6th 2023, unfortunately Bard still makes a lot of mistakes"""
        # Check rows
        for row in self.board:
            if all(symbol == "X" for symbol in row):
                return "X"
            elif all(symbol == "O" for symbol in row):
                return "O"

        # Check columns
        for col_index in range(3):
            if all(row[col_index] == "X" for row in self.board):
                return "X"
            elif all(row[col_index] == "O" for row in self.board):
                return "O"

        # Check diagonals
        if all(self.board[i][i] == "X" for i in range(3)):
            return "X"
        elif all(self.board[i][2 - i] == "X" for i in range(3)):
            return "X"
        elif all(self.board[i][i] == "O" for i in range(3)):
            return "O"
        elif all(self.board[i][2 - i] == "O" for i in range(3)):
            return "O"

        return "_"  # Ongoing or draw game

    def game_over(self) -> bool:
        winner = self.winner
        if winner in ['X', 'O']:
            return True
        if len(self.actions) == 0:
            return True
        return False

    @property
    @cache
    def actions(self) -> tuple[Action, ...]:
        actions: list[Action] = []
        for row, col in product(range(3), range(3)):
            if self.board[row][col] == '_':
                actions.append((row, col))
        return tuple(actions)

    def apply(self, action: Action) -> State:
        symbol = self.current_player
        row, col = action
        board_copy = [list(tup) for tup in self.board]
        board_copy[row][col] = symbol
        next_player: Symbol = 'O' if self.current_player == 'X' else 'X'
        result_board = tuple(tuple(lst) for lst in board_copy)
        return State(board = result_board, current_player = next_player) # type: ignore Static type checker fails to detect length of tuple

    @staticmethod
    def initial() -> State:
        initial_board = (   ('_', '_', '_'),
                            ('_', '_', '_'),
                            ('_', '_', '_'))
        return State(board = initial_board, current_player = 'X') # type: ignore

    def __str__(self):
        rows = [' | '.join([' ' if s == '_' else s for s in r]) for r in self.board]
        spacer = '\n---------\n'
        return spacer.join(rows)