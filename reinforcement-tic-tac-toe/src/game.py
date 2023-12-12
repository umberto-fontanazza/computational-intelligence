from typing import Literal
from src.agent import Agent
from src.state import State
from src.policy import Policy

def play_game(learning_agent: Agent, opponent: Policy, agent_starts = True, training = False) -> Literal['Win', 'Loss', 'Draw']:
    """A learning agent faces an opponent in a tic-tac-toe game. """
    state = State.initial()
    agent = learning_agent
    agent.reset()
    epsilon = .05 if training else None

    if not agent_starts:
        state = state.apply(opponent(state))

    while(True):
        # agent turn
        if state.game_over():
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