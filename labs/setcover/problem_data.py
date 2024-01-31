from random import random
from numpy import array

PROBLEM_SIZE = 500
NUM_SETS = 10_000
SETS = tuple(
    array([random() < 0.3 for _ in range(PROBLEM_SIZE)])
    for _ in range(NUM_SETS)
)
