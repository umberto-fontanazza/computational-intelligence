from dataclasses import dataclass

@dataclass(frozen=True)
class Move():
    row: int
    quantity: int