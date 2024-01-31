from __future__ import annotations
from src.chromosome import Chromosome, Mask
from typing import Callable, Literal
from dataclasses import dataclass
from random import choice, choices, randint, shuffle
from functools import cache

@dataclass(frozen=True)
class Genome():
    genes: tuple[int, ...]
    fitness_fn: Callable[[list[int]], float]

    # TODO: chromosome rct

    @staticmethod
    def random(length: int, fitness_fn: Callable[[list[int]], float]) -> Genome:
        return Genome(tuple(gene for gene in choices([0, 1], k = length)), fitness_fn)

    def combine_masked(self, other: Genome, mask: Mask) -> Genome:
        """Self.genes marked by positive values of mask are applied to a copy of other"""

        child_genome = [gene if mask[i] else other.genes[i] for i, gene in enumerate(self.genes)]
        return Genome(tuple(child_genome), self.fitness_fn)

    def combine(self, other: Genome, strategy: Literal['mix', 'one cut', 'two cuts'] = 'mix') -> Genome:
        length = len(self.genes)
        if strategy not in ['mix', 'one cut']:
            raise ValueError(f'Strategy {strategy} not valid')
        if strategy == 'mix':
            child_genes = tuple(choice([self.genes[i], other.genes[i]]) for i in range(length))
            return Genome(child_genes, self.fitness_fn)
        if strategy == 'one cut': # deprecated, close genes are changed toghether
            cut_index = randint(1, length - 1)
            child_genes = self.genes[:cut_index] + other.genes[cut_index:length]
            return Genome(child_genes, self.fitness_fn)
        if strategy == 'two cuts': # deprecated, close genes are changed toghether
            if len(self.genes) < 3:
                raise ValueError('Genome too short, two cuts not applicable')
            cut_index_one = cut_index_two = randint(1, length - 1)
            while cut_index_two == cut_index_one:
                cut_index_two = randint(1, length - 1)
            if cut_index_two < cut_index_one:
                cut_index_one, cut_index_two = cut_index_two, cut_index_one
            child_genes = self.genes[:cut_index_one] + other.genes[cut_index_one:cut_index_two] + self.genes[cut_index_two:]
            return Genome(tuple(child_genes), self.fitness_fn)

    def chromosome_fitness_gain(self, mask: Mask, random_genomes: list[Genome]) -> float:
        """Measure the gain of applying the chromosome identified by the mask to a pool of random genomes"""

        previous_average_fitness = sum([genome.fitness for genome in random_genomes]) / len(random_genomes)
        random_with_chromosome = [self.combine_masked(other, mask) for other in random_genomes]
        updated_average_fitness = sum([genome.fitness for genome in random_with_chromosome]) / len(random_with_chromosome)
        return updated_average_fitness - previous_average_fitness

    def simple_mutate(self) -> Genome:
        length = len(self.genes)
        changing_index = randint(0, length - 1)
        child_genes = tuple(gene ^ 1 if i == changing_index else gene for i, gene in enumerate(self.genes))
        return Genome(child_genes, self.fitness_fn)

    def mutate(self) -> Genome:
        """Swap a number of genes(loci) proportional to the distance from perfect fitness(=1)"""

        best_fitness_distance = 1 - self.fitness
        genome_length = len(self.genes)
        mutations_count = round(genome_length * best_fitness_distance) or 1
        mutations_mask = [True if i < mutations_count else False for i in range(genome_length)]
        shuffle(mutations_mask)
        child_genome = tuple((gene ^ 1) if mutations_mask[i] else gene for i, gene in enumerate(self.genes))
        return Genome(child_genome, self.fitness_fn)

    def climb_hill(self, max_steps = 100, max_non_improving_steps = 5, λ = 3) -> Genome:
        """Optimizes local optimum, + strategy hill climber.
        λ is the number of children, μ = 1"""

        previous_fittest = None
        fittest: Genome = self
        non_improving_steps = 0
        for _ in range(max_steps):
            children = [self.mutate() for _ in range(λ)]
            previous_fittest = fittest
            fittest = max([fittest, *children], key = lambda genome: genome.fitness)
            if fittest.fitness == previous_fittest.fitness:
                non_improving_steps += 1
            else:
                non_improving_steps = 0
            if non_improving_steps == max_non_improving_steps:
                break
        return fittest

    def __str__(self) -> str:
        return f"{''.join([str(gene) for gene in self.genes])}, fitness: {self.fitness:3.2%}"

    @property
    @cache
    def fitness(self) -> float:
        genes_list: list[int] = [x for x in self.genes]
        return self.fitness_fn(genes_list)

    def distance(self, other: Genome, method: Literal['relative', 'absolute'] = 'relative') -> float | int:
        """method = 'absolute' returns int number of different genes, method = 'relative' returns float ratio
        (absolute distance / genome length)"""

        if len(self.genes) != len(other.genes):
            raise ValueError('Cannot evaluate distance between genomes of different length')
        differences = 0
        for i in range(len(self.genes)):
            if self.genes[i] != other.genes[i]:
                differences += 1
            # benchmark against
            # differences += self.genes[i] ^ other.genes[i]
        if method == 'absolute':
            return differences
        elif method == 'relative':
            return differences / len(self.genes)

    def extract_chromosome(self, mask: Mask) -> Chromosome:
        """Extract a chromosome from genome"""
        return Chromosome(self.genes, mask)

    def assign_chromosome(self, mutation: Chromosome) -> Genome:
        """Returns a new Genome featuring the mutation Chromosome"""

        mutated_genes = tuple(mutation.genes[i] if mutation.mask[i] else gene for i, gene in enumerate(self.genes))
        return Genome(mutated_genes, self.fitness_fn)