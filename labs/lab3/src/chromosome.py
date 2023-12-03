from dataclasses import dataclass
from typing import Literal

Mask = tuple[bool, ...] | tuple[Literal[0,1], ...]

@dataclass(frozen = True)
class Chromosome():
    genes : tuple[int, ...]
    mask : Mask