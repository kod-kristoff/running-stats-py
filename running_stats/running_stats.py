"""Compute mean and variance."""
import math
import typing

import attr


@attr.s(auto_attribs=True)
class RunningMeanVar:
    """Compute mean and variance."""

    n: int = 0
    M1: float = 0.0
    M2: float = 0.0

    def push(self, value: float) -> None:
        """Add a value."""
        self.n += 1
        delta = value - self.M1
        self.M1 += delta / self.n
        self.M2 += delta * (value - self.M1)

    def push_iter(self, values: typing.Iterable[float]):
        """Add values from an Iterable."""
        for value in values:
            self.push(value)

    def mean(self) -> float:
        """Compute mean."""
        return self.M1

    def variance(self) -> float:
        """Compute the sample variance."""
        return self.M2 / (self.n - 1) if self.n > 1 else 0.0

    def standard_deviation(self) -> float:
        """Compute the sample standard deviation."""
        return math.sqrt(self.variance())

    def __add__(self, other):
        combined = RunningMeanVar()
        combined.n = self.n + other.n

        delta = other.M1 - self.M1
        delta2 = delta * delta

        combined.M1 = (self.M1 * self.n + other.M1 * other.n) / combined.n
        combined.M2 = self.M2 + other.M2 + delta2 * self.n * other.n / combined.n

        return combined
