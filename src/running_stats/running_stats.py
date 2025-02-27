"""Compute mean and variance."""
import math
import typing

import attr


@attr.s(auto_attribs=True)
class RunningMeanVar:
    """Compute mean and variance.
    """
    num_values: int = 0
    M1: float = 0.0
    M2: float = 0.0

    def push(self, value: float) -> None:
        """Add a value."""
        self.num_values += 1
        delta = value - self.M1
        self.M1 += delta/self.num_values
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
        return self.M2/(self.num_values - 1) if self.num_values > 1 else 0.0

    def standard_deviation(self) -> float:
        """Compute the sample standard deviation."""
        return math.sqrt(self.variance())

    def __add__(self, other):
        combined = RunningMeanVar()
        combined.num_values = self.num_values + other.num_values

        delta = other.M1 - self.M1
        delta2 = delta * delta

        combined.M1 = (self.M1 * self.num_values + other.M1 * other.num_values)/combined.num_values
        combined.M2 = self.M2 + other.M2 + delta2 * self.num_values * other.num_values / combined.num_values

        return combined


@attr.s(auto_attribs=True)
class RunningStats(RunningMeanVar):
    M3: float = 0.0
    M4: float = 0.0

    def push(self, x: float) -> None:
        n_1 = self.num_values
        self.num_values += 1
        delta = x - self.M1
        delta_n = delta / self.num_values
        delta_n2 = delta_n * delta_n
        term1 = delta * delta_n * n_1
        self.M1 += delta_n
        self.M4 += term1 * delta_n2 * (self.num_values*self.num_values - 3*self.num_values + 3) + 6 * delta_n2 * self.M2 - 4 * delta_n * self.M3
        self.M2 += term1
