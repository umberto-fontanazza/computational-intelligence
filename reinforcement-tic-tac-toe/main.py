from typing import Callable
from dataclasses import replace
from src.agent import Agent
from src.state import State, Action
from random import choice

def fixed_policy(board: State) -> Action:
    """A simple policy for making a move, aka non learning agent"""

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

def policy_ask_input(board: State) -> Action:
    print(board, '\n')
    for i, action in enumerate(board.actions):
        print(f'Action {i}: {action}')
    print()

    move = -1
    while move not in range(len(board.actions)):
        move = int(input('Pick move: '))
    return board.actions[move]


def play_game(player_one_policy: Callable[[State], Action], player_two_policy: Callable[[State], Action]):
    s = State.initial()

    while(True):
        s = s.apply(player_one_policy(s)) # policy plays

        if s.game_over():
            print('Game over')
            print(s)
            break

        selected_action = player_two_policy(s)
        s = s.apply(selected_action)

        if s.game_over():
            print('Game over')
            print(s)
            break


def main():
    a = Agent()

    training_games = 5000
    for i in range(training_games):
        state = State.initial()
        if i % 2 == 0:
            policy_move = fixed_policy(state)
            state = state.apply(policy_move)

        while(True): # game loop
            if state.game_over():
                if state.winner == state.current_player:
                    reward = 15
                elif state.winner == '_':
                    reward = 0
                else:
                    reward = -20
                a.input(None, reward)
                break

            a.input(state, reward=0)
            agent_move = a.move(state, epsilon=.1)
            state = state.apply(agent_move)

            if state.game_over():
                continue
            policy_move = fixed_policy(state)
            state = state.apply(policy_move)

    play_game(a.policy, policy_ask_input)

if __name__ == '__main__':
    main()