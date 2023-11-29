from __future__ import annotations
from dataclasses import dataclass
from src.genome import Genome
from random import choices

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
        children = [couple[0].combine(couple[1]) for couple in couples]
        return children

    def next_generation(self) -> Population:
        population_size = len(self.genomes)
        children = self.recombination(20)
        optimized_children = [child.climb_hill() for child in children]
        selection_pool: list[Genome] = sorted([*self.genomes, *optimized_children], key= lambda genome: genome.fitness, reverse=True)
        return Population(selection_pool[0: population_size])

    def best_genome(self) -> Genome:
        return max(self.genomes, key = lambda genome: genome.fitness)