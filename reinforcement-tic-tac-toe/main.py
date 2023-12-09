from typing import Callable
from dataclasses import replace
from src.agent import Agent
from src.state import State, Action
from random import choice

def policy(board: State) -> Action:
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

def play_game(policy: Callable[[State], Action]):
    s = State.initial()

    while(True):
        s = s.apply(policy(s)) # policy plays

        if s.game_over():
            print('Game over')
            print(s)
            break

        for i, action in enumerate(s.actions):
            print()
            print(f' Action {i}: {action} ', end=None)
        selected_action_i = -1
        while(selected_action_i not in range(len(s.actions))):
            print(s)
            prompt = 'Select an action: '
            selected_action_i : int = int(input(prompt))
            selected_action = s.actions[selected_action_i]
            s = s.apply(selected_action)

        if s.game_over():
            print('Game over')
            print(s)
            break


def main():
    a = Agent()

    training_games = 10
    for i in range(training_games):
        state = State.initial()
        if i % 2 == 0:
            policy_move = policy(state)
            state = state.apply(policy_move)

        while(True): # game loop
            if state.game_over():
                if state.winner == state.current_player:
                    reward = 15
                elif state.winner == '_':
                    reward = 0
                else:
                    reward = -10
                a.input(None, reward)
                break

            a.input(state, reward=0)
            agent_move = a.move(state, epsilon=.1)
            state = state.apply(agent_move)

            if state.game_over():
                continue
            policy_move = policy(state)
            state = state.apply(policy_move)

    play_game(a.policy)

if __name__ == '__main__':
    main()