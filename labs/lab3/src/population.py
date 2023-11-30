from __future__ import annotations
from typing import Callable
from dataclasses import dataclass
from src.genome import Genome
from random import choices
from functools import cache

'''Selects from the population a number of {selected_count} individuals'''
def tournament_selection(population: list[Genome], selected_count: int, tournament_size = 2) -> list[Genome]:
    contendants: list[Genome] = choices(population, k= selected_count * tournament_size)
    torunaments = [tuple(contendants[i:(i + tournament_size)]) for i in range(selected_count)]
    winners = [max(t, key= lambda g: g.fitness) for t in torunaments]
    return winners

@dataclass
class Population:
    genomes: list[Genome]

    '''Tournament selection of size 2 determines parents, which are coupled and combined'''
    def recombination(self, children_count: int) -> list[Genome]:
        parent_count = children_count * 2 # two parent x-over
        parents = tournament_selection(self.genomes, selected_count = parent_count)
        couples = [tuple(parents[i:(i + 2)]) for i in range(children_count)]
        couples = [couple for couple in couples if couple[0]!=couple[1]] # recombining element with itself makes no sense
        children = [couple[0].combine(couple[1]) for couple in couples]
        return children

    def next_generation(self) -> Population:
        population_size = len(self.genomes)
        children = self.recombination(20)
        optimized_children = [child.climb_hill() for child in children]
        selection_pool: list[Genome] = sorted(self.genomes + optimized_children, key= lambda genome: genome.fitness, reverse=True) # [*self.genomes, *optimized_children]
        return Population(selection_pool[0: population_size])

    @property
    # @cache TODO: in order to use population must be hashable
    def best_genome(self) -> Genome:
        return max(self.genomes, key = lambda genome: genome.fitness)

    '''The initial population is not made of random genomes but of genomes locally optimized,
    where locally optimized means they are the result of an hill climber'''
    @staticmethod
    def initial(genome_size: int, fitness_fn: Callable[[list[int]], float], population_size = 30) -> Population:
        population = [Genome.random(genome_size, fitness_fn) for _ in range(population_size)]
        climbers = [genome.climb_hill() for genome in population]
        return Population(climbers)
