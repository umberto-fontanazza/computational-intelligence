from dataclasses import dataclass
from strategy import Strategy

TOTAL_STRATEGIES = 5

available_strategies: list[Strategy] = Strategy.all()
strategies_count = len(available_strategies)

@dataclass(frozen=True)
class State():
    strategy_probability: list[float] = [1 / strategies_count for _ in range(strategies_count)] # uniform probability distribution
    strategies: list[Strategy] = available_strategies