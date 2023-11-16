from src.state import State
from src.strategy import Strategy
from src.game import Game
from itertools import product

def confront_strategies(player: Strategy, opponent: Strategy, games_number = 100):
    wins = 0
    for player_starts, _ in product([False, True], range(games_number // 2)):
        game = Game(4, player, opponent, player_starts)
        try:
            if game.player_wins():
                wins += 1
        except ValueError:
            pass
    losses = games_number - wins
    print(f'{player}: {wins},  {opponent}: {losses}')

def main():
    initial_state = State()
    steps = 100

    current_state, current_fitness = initial_state, initial_state.fitness()
    print(current_state)
    for _ in range(steps):
        # 1 + 3 evolution strategy
        parent = current_state
        μ, λ = 1, 3
        for i in range(λ):
            child = parent.mutate()
            child_fit = child.fitness()
            if(child_fit > current_fitness):
                current_state = child
                current_fitness = child_fit
        print(f'Fit: {current_fitness}')
    print(current_state)

if __name__ == '__main__':
    # main()
    confront_strategies(Strategy.expert_system(), Strategy.optimal())