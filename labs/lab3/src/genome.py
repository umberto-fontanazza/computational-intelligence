from __future__ import annotations
from typing import Callable, Literal
from dataclasses import dataclass
from random import choice, choices, randint, shuffle
from functools import cache

@dataclass(frozen=True)
class Genome():
    genes: tuple[int, ...]
    fitness_fn: Callable[[list[int]], float]

    @staticmethod
    def random(length: int, fitness_fn: Callable[[list[int]], float]) -> Genome:
        return Genome(tuple(gene for gene in choices([0, 1], k = length)), fitness_fn)

    # TODO: add two cuts
    def combine(self, other: Genome, strategy: Literal['mix', 'one cut'] = 'mix') -> Genome:
        length = len(self.genes)
        if strategy not in ['mix', 'one cut']:
            raise ValueError(f'Strategy {strategy} not valid')
        if strategy == 'mix':
            child_genes = tuple(choice([self.genes[i], other.genes[i]]) for i in range(length))
            return Genome(child_genes, self.fitness_fn)
        if strategy == 'one cut':
            cut_index = randint(1, length - 1)
            child_genes = self.genes[:cut_index] + other.genes[cut_index:length]
            return Genome(child_genes, self.fitness_fn)

    def mutate(self) -> Genome:
        length = len(self.genes)
        changing_index = randint(0, length - 1)
        child_genes = tuple(gene ^ 1 if i == changing_index else gene for i, gene in enumerate(self.genes))
        return Genome(child_genes, self.fitness_fn)

    '''Exploit solvability of the problem, we know max fitness is 1 and minimum fitness is 0
    Mutate a quantity of genes(loci) proportional to the distance from perfect fitness'''
    def mutate2(self) -> Genome:
        best_fitness_distance = 1 - self.fitness
        genome_length = len(self.genes)
        mutations_count = round(genome_length * best_fitness_distance)
        mutations_mask = [True if i < mutations_count else False for i in range(genome_length)]
        shuffle(mutations_mask)
        child_genome = tuple((gene ^ 1) if mutations_mask[i] else gene for i, gene in enumerate(self.genes))
        return Genome(child_genome, self.fitness_fn)

    def __str__(self) -> str:
        return ''.join([str(gene) for gene in self.genes])

    @property
    @cache
    def fitness(self) -> float:
        return self.fitness_fn([x for x in self.genes])