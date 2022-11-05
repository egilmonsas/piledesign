from dataclasses import dataclass

from typing_extensions import Self


@dataclass
class Coordinate:
    x: float
    y: float

    def compute_distance(self, other: Self):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
