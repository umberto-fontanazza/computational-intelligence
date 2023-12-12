from typing import Literal
from src.agent import Agent
from src.state import State
from src.policy import Policy, random_policy, simple_policy, human_policy

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


def main():
    agent = Agent()
    opponent = random_policy
    agent_starts = True
    training_games = 10_000
    testing_games = 100

    # train
    for _ in range(training_games):
        play_game(agent, opponent, training = True, agent_starts = agent_starts)

    # test
    wins = losses = 0
    for _ in range(testing_games):
        outcome = play_game(agent, simple_policy, agent_starts = agent_starts)
        if outcome == 'Win':
            wins += 1
        elif outcome == 'Loss':
            losses += 1

    print(f'Out of {testing_games}, agent performed {wins} wins and {losses} losses.')

if __name__ == '__main__':
    main()