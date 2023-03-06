from __future__ import annotations
from enum import Enum
from typing import List, NamedTuple, Callable, Optional, Tuple
import random
from math import sqrt
from generic_search import dfs, bfs, node_to_path, astar, Node
import matplotlib.pyplot as plt


def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = ml.column - goal.column
        ydist: int = ml.row - goal.row
        return sqrt((xdist * xdist) + (ydist * ydist))
    return distance


def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.column - goal.column)
        ydist: int = abs(ml.row - goal.row)
        return (xdist + ydist)
    return distance


class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"


class MazeLocation(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(self, rows: int = 10, columns: int = 10, sparseness: float = 0.2, start: MazeLocation = MazeLocation(0, 0), goal: MazeLocation = MazeLocation(9, 9)) -> None:
        self._rows = rows
        self._columns = columns
        self.start = start
        self.goal = goal
        self._grid: List[List[Cell]] = [
            [Cell.EMPTY for c in range(columns)] for r in range(rows)]
        self._randomly_fill(rows, columns, sparseness)
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0.0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    def goal_test(self, ml: MazeLocation) -> bool:
        return ml == self.goal

    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        locations: List[MazeLocation] = []
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if ml.column + 1 < self._columns and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations

    def mark(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def __str__(self) -> str:
        output: str = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output


def benchmark(trails: int):
    dfs_trails = []
    bfs_trails = []
    astar_trails = []
    for _ in range(trails):
        maze: Maze = Maze()

        dfs_wrapper: Tuple[Optional[Node[MazeLocation]], int] = dfs(
            maze.start, maze.goal_test, maze.successors)
        _, dfs_count = dfs_wrapper
        dfs_trails.append(dfs_count)

        bfs_wrapper: Tuple[Optional[Node[MazeLocation]], int] = bfs(
            maze.start, maze.goal_test, maze.successors)
        _, bfs_count = bfs_wrapper
        bfs_trails.append(bfs_count)

        distance: Callable[[MazeLocation],
                           float] = manhattan_distance(maze.goal)
        astar_wrapper: Tuple[Optional[Node[MazeLocation]], int] = astar(
            maze.start, maze.goal_test, maze.successors, distance)
        _, astar_count = astar_wrapper
        astar_trails.append(astar_count)

    fig, axs = plt.subplots(1, 3, sharey=True, tight_layout=True)
    n_bins = int(trails / 20)

    axs[0].hist(dfs_trails, bins=n_bins)
    axs[0].set_title("DFS")
    axs[1].hist(bfs_trails, bins=n_bins)
    axs[1].set_title("BFS")
    axs[2].hist(astar_trails, bins=n_bins)
    axs[2].set_title("A*")

    plt.show()


if __name__ == "__main__":
    BENCHMARK = True
    if BENCHMARK:
        benchmark(1000)
    else:
        maze: Maze = Maze()
        print(maze)
        solution1_wrapper: Tuple[Optional[Node[MazeLocation]], int] = dfs(
            maze.start, maze.goal_test, maze.successors)
        solution1, count = solution1_wrapper
        if solution1 is None:
            print("Couldn't find a solution with dfs!")
        else:
            path1: List[MazeLocation] = node_to_path(solution1)
            maze.mark(path1)
            print("dfs solution:")
            print(maze)
            maze.clear(path1)

        solution2_wrapper: Tuple[Optional[Node[MazeLocation]], int] = bfs(
            maze.start, maze.goal_test, maze.successors)
        solution2, count = solution2_wrapper
        if solution2 is None:
            print("Couldn't find a solution with bfs!")
        else:
            path2: List[MazeLocation] = node_to_path(solution2)
            maze.mark(path2)
            print("bfs solution:")
            print(maze)
            maze.clear(path2)

        distance: Callable[[MazeLocation],
                           float] = manhattan_distance(maze.goal)
        solution3_wrapper: Tuple[Optional[Node[MazeLocation]], int] = astar(
            maze.start, maze.goal_test, maze.successors, distance)
        solution3, count = solution3_wrapper
        if solution3 is None:
            print("Couldn't find a solution with A*!")
        else:
            path3: List[MazeLocation] = node_to_path(solution3)
            maze.mark(path3)
            print("A* solution:")
            print(maze)
