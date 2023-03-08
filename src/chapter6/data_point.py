from __future__ import annotations
from typing import Iterator, Tuple, List, Iterable
from math import sqrt


class DataPoint:
    def __init__(self, initial: Iterable[float]) -> None:
        self._originals: Tuple[float, ...] = tuple(initial)
        self.dimensions: Tuple[float, ...] = tuple(initial)

    @property
    def num_dimensions(self) -> int:
        return len(self.dimensions)

    def distance(self, other: DataPoint) -> float:
        combined: Iterator[Tuple[float, float]] = zip(
            self.dimensions, other.dimensions)
        differences: List[float] = [(x - y) ** 2.0 for x, y in combined]
        return sqrt(sum(differences))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataPoint):
            return NotImplemented  # Why are we doing this? Let's just type the function as DataPoint?
        return self.dimensions == other.dimensions

    def __repr__(self) -> str:
        return self._originals.__repr__()
