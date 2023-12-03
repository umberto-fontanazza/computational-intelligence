from src.genome import Genome
from src.chromosome import Chromosome

def simple_fitness(genes: list[int]):
    return sum(genes) / len(genes)

def test_extract_chromosome():
    g = Genome((0,1,1,1,0), simple_fitness)
    chromosome = g.extract_chromosome((1,1,0,0,0))

    assert chromosome.mask == (1,1,0,0,0)
    assert chromosome.genes == g.genes