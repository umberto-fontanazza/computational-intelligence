from __future__ import annotations
from dataclasses import dataclass
from numpy import array, logical_or, bool_
from numpy.typing import NDArray
from functools import reduce, cache
from problem_data import PROBLEM_SIZE

@dataclass(frozen=True)
class State():
    current_cost: int
    taken : tuple[NDArray[bool_] | None]
    not_taken : tuple[NDArray[bool_]]

    # read docs first but @cache is a good idea
    def __current_coverage(self) -> NDArray[bool_]:
        if not self.taken: return array([False for _ in range(PROBLEM_SIZE)])
        return reduce(logical_or, self.taken)

    def is_solution(self) -> bool:
        return all(self.__current_coverage())

    def take_covering_set(self, covering_set: NDArray[bool_]) -> State:
        new_state_take : tuple[NDArray[bool_]] = (*self.taken, covering_set)
        return State(
            current_cost = self.current_cost + 1,
            taken = (*self.taken, covering_set),
            not_taken = tuple(x for x in self.not_taken if x != covering_set)
        )

    def estimated_additional_cost(self) -> int:
        return 1 # doesn't help to discard some branches but it's admissible

    def estimated_total_cost(self) -> int:
        return self.current_cost + self.estimated_additional_cost()

    def fitness(self) -> tuple[int, int] :
        current_coverage_size = sum(self.__current_coverage)
        return (current_coverage_size, -self.current_cost)

    @staticmethod
    def initial(available_sets: tuple[NDArray[bool_]]):
        return State(current_cost = 0,
                     taken = (),
                     not_taken = available_sets)

