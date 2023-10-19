from __future__ import annotations
from dataclasses import dataclass
from numpy import array, logical_or
from functools import reduce, cache

@dataclass(frozen=True)
class State():
    current_cost: int
    taken : tuple[array[bool]]
    not_taken : tuple[array[bool]]

    # read docs first but @cache is a good idea
    def __current_coverage(self) -> array[bool]:
        return reduce(logical_or, self.taken)

    def is_solution(self) -> bool:
        return all(self.__current_coverage())

    def take_covering_set(self, covering_set: array[bool]) -> State:
        return State(
            current_cost = self.current_cost + 1,
            taken = (*self.taken, covering_set),
            not_taken = tuple([x for x in self.not_taken if x != covering_set])
        )

    def estimated_additional_cost(self) -> int:
        # TODO: to be implemented
        raise NotImplementedError()

    def estimated_total_cost(self) -> int:
        return self.current_cost + self.estimated_additional_cost()