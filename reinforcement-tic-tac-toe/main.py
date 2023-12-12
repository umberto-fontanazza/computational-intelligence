from typing import Callable, Literal
from dataclasses import replace
from src.agent import Agent
from src.state import State, Action
from random import choice

def random_move(board: State) -> Action:
    return choice(board.actions)

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


def play_game(learning_agent: Agent, opponent: Callable[[State], Action], agent_starts = True, training = False, debug = False) -> Literal['Win', 'Loss', 'Draw']:
    """Agent wins = return value"""
    state = State.initial()
    agent = learning_agent
    agent.reset()
    epsilon = .05 if training else None

    if not agent_starts:
        state = state.apply(opponent(state))

    while(True):
        # agent turn
        if state.game_over():
            if debug:
                print('\n','Game over:')
                print(state)
            if not training:
                break
            if state.winner == '_': # draw
                agent.input(new_state = None, reward = 0)
            else: # agent loss
                agent.input(new_state = None, reward = -15)
            break
        agent.input(state, reward = 0)
        state = state.apply(agent.move(state, epsilon=epsilon))

        # opponent turn
        if state.game_over():
            if debug:
                print('\n', 'Game over:')
                print(state)
            if not training:
                break
            if state.winner == '_': # draw
                agent.input(new_state = None, reward = 0)
            else: # agent won
                agent.input(new_state = None, reward = 15)
            break
        state = state.apply(opponent(state))

    if agent_starts and state.winner == 'X':
        return 'Win'
    if not agent_starts and state.winner == 'O':
        return 'Win'
    elif state.winner == '_':
        return 'Draw'
    else:
        return 'Loss'


def main():
    agent = Agent()
    opponent = fixed_policy
    agent_starts = False

    # train
    for i in range(100000):
        play_game(agent, opponent, training = True, agent_starts=agent_starts)

    # test
    test_games = 50
    wins = losses = 0
    for i in range(test_games):
        outcome = play_game(agent, opponent, debug = False, agent_starts=agent_starts)
        if outcome == 'Win':
            wins += 1
        elif outcome == 'Loss':
            losses += 1

    print(f'Out of {test_games}, agent performed {wins} wins and {losses} losses.')

if __name__ == '__main__':
    main()