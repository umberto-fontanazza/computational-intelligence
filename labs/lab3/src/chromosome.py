from dataclasses import dataclass
from typing import Literal

@dataclass(frozen = True)
class Chromosome():
    genes : tuple[int, ...]
    mask : tuple[bool, ...] | tuple[Literal[0,1], ...]