from src.agent import Agent
from src.policy import Policy, random_policy, simple_policy, human_policy
from src.game import play_game

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