from typing import Callable
from src.state import State, Action
from random import choice
from dataclasses import replace

Policy = Callable[[State], Action]

def random_policy(board: State) -> Action:
    return choice(board.actions)

def simple_policy(board: State) -> Action:
    """A simple policy for making a move."""

    # Check if there's a winning move
    for action in board.actions:
        if board.apply(action).game_over():
            return action

    # If there's no winning move, block the opponent's winning move
    opponent_turn = replace(board, current_player = 'O' if board.current_player == 'O' else 'X')
    for action in opponent_turn.actions:
        if opponent_turn.apply(action).game_over():
            return action

    # If there's no move to win or block, make a random move
    return choice(board.actions)

def human_policy(board: State) -> Action:
    """Ask a human to imput the move"""
    print(board, '\n')
    for i, action in enumerate(board.actions):
        print(f'Action {i}: {action}')
    print()

    move = -1
    while move not in range(len(board.actions)):
        move = int(input('Pick move: '))
    return board.actions[move]