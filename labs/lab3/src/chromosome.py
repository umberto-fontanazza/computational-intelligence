from dataclasses import dataclass
from typing import Literal

Mask = tuple[bool, ...] | tuple[Literal[0,1], ...]

@dataclass(frozen = True)
class Chromosome():
    genes : tuple[int, ...]
    mask : Mask
    fitness_samples: list[float] = []

    def add_fitness_sample(self, *args: float):
        for arg in args:
            self.fitness_samples.append(arg)

    @property
    def fitness(self) -> float:
        return sum(self.fitness_samples) / len(self.fitness_samples)