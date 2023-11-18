from __future__ import annotations
from dataclasses import dataclass
from src.state import State
from random import choices

@dataclass(frozen=True)
class Generation():
    μ: int = 20
    λ: int = 30
    # this must be sorted in descending fitness
    population: tuple[State, ...] = tuple(State() for _ in range(μ))

    def offspring(self) -> tuple[State, ...]:
        random_parents = choices(self.population, k=self.λ)
        return tuple(parent.mutate() for parent in random_parents)

    def next(self) -> Generation:
        offspring = self.offspring()
        candidates: tuple[State, ...] = self.population + offspring
        ranked_candidates = sorted(candidates, key=lambda state: state.fitness(), reverse=True)
        fittest = tuple(ranked_candidates[:self.μ])
        return Generation(self.μ, self.λ, fittest)

    def fittest_individual(self) -> State:
        return self.population[0]


