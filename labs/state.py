from __future__ import annotations
from dataclasses import dataclass
from strategy import Strategy
from random import randint
from numpy.random import choice
from itertools import product
from game import Game

available_strategies: list[Strategy] = Strategy.all()
strategies_count = len(available_strategies)

def normalized(probability_weights: list[float]) -> list[float]:
    norm_one = sum(probability_weights)
    return [x / norm_one for x in probability_weights]

def uniform_distribution(size: int) -> list[float]:
    return [1/ size for _ in range(size)]

@dataclass(frozen=True)
class State():
    strategy_probability: tuple[float, ...] = tuple(uniform_distribution(strategies_count))
    strategies: tuple[Strategy, ...] = tuple(available_strategies)

    def mutate(self) -> State:
        mutating_index = randint(0, strategies_count - 1)
        sigma = 0.5 # TODO: make it random distribution
        child_probabilities = [x + sigma if i == mutating_index else x for i,x in enumerate(self.strategy_probability)]
        child_probabilities = normalized(child_probabilities)
        return State(tuple(child_probabilities), self.strategies)

    def pick_strategy(self) -> Strategy:
        strategy_index = choice(strategies_count, p = self.strategy_probability)
        return self.strategies[strategy_index]

    @staticmethod
    def crossover(first_parent: State, second_parent: State) -> State:
        raise NotImplementedError()

    def fitness(self, nim_rows = 4):
        # play 10 games against gabriele
        num_games = 100
        opponent = Strategy.gabriele()
        victories, total_games = 0, 0
        for play_first, game_number in product([True, False], range(1, num_games // 2 + 1)):
            player = self.pick_strategy()
            game = Game(nim_rows, player, opponent, play_first)
            if game.player_wins():
                victories += 1
            total_games += 1
        return victories / total_games

    def __str__(self) -> str:
        ret = '\n'
        for i, strat in enumerate(self.strategies):
            ret = ret + f'{strat.name}   {self.strategy_probability[i]:.2f}\n'
        return ret