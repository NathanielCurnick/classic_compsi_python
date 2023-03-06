import matplotlib.pyplot as plt
from typing import List
import math


def gregory_leibniz(n_terms: int) -> List[float]:
    attempts: List[float] = []
    numerator: float = 4.0
    denominator: float = 1.0
    operation: float = 1.0
    pi: float = 0.0
    for _ in range(n_terms):
        pi += operation * (numerator / denominator)
        denominator += 2.0
        operation *= -1.0
        attempts.append(pi)

    return attempts


def nilakantha(n_terms: int) -> List[float]:
    attempts: List[float] = []
    pi: float = 3.0
    alpha: float = 2.0
    beta: float = 3.0
    gamma: float = 4.0
    operation = 1.0

    for _ in range(n_terms):
        pi += operation * (4.0 / (alpha * beta * gamma))
        alpha += 2.0
        beta += 2.0
        gamma += 2.0
        operation *= -1.0
        attempts.append(pi)

    return attempts


if __name__ == "__main__":
    trails = 100
    gl = gregory_leibniz(trails)
    ni = nilakantha(trails)

    plt.figure()
    plt.plot(gl, label="Gregory-Leibniz", color="blue")
    plt.plot(ni, label="Nilakantha", color="green")
    plt.axhline(math.pi, label="Pi (from math library)",
                linestyle="dashed", color="red")
    plt.legend()
    plt.show()
