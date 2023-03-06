from typing import List
import matplotlib.pyplot as plt


def fibonacci(n: int) -> List[int]:

    fibs = [0, 1]

    def fib(n: int) -> int:
        if n == 0:
            return n  # special case
        last: int = 0  # initially set to fib(0)
        next: int = 1  # initially set to fib(1)
        for _ in range(1, n):
            last, next = next, last + next
            fibs.append(next)
        return next

    fib(n)

    return fibs


def plot_fib(fibs: List[int]):
    index = range(0, len(fibs))
    plt.bar(index, fibs)
    plt.show()


if __name__ == "__main__":
    fibs = fibonacci(20)
    print(fibs)
    plot_fib(fibs)
