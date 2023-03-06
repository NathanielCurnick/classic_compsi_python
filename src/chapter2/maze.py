from __future__ import annotations
from enum import Enum
from typing import List, NamedTuple, Callable, Optional, Generic, TypeVar, Set, Deque
import random
from heapq import heappush, heappop
from math import sqrt
# from generic_search import dfs, bfs, node_to_path, astar, Node


T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = Deque()

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()

    def __repr__(self) -> str:
        return repr(self._container)


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        heappush(self._container, item)

    def pop(self) -> T:
        return heappop(self._container)

    def __repr__(self) -> str:
        return repr(self._container)


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


class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0, heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def dfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    # frontier is where we've yet to go
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    # explored is where we've been
    explored: Set[T] = {initial}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't explored
        for child in successors(current_state):
            if child in explored:  # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None  # went through everything and never found goal


def bfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    # frontier is where we've yet to go
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # explored is where we've been
    explored: Set[T] = {initial}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't explored
        for child in successors(current_state):
            if child in explored:  # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None  # went through everything and never found goal


def astar(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]], heuristic: Callable[[T], float]) -> Optional[Node[T]]:
    # frontier is where we've yet to go
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    # explored is where we've been
    explored: Dict[T, float] = {initial: 0.0}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't explored
        for child in successors(current_state):
            # 1 assumes a grid, need a cost function for more sophisticated apps
            new_cost: float = current_node.cost + 1

            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node,
                              new_cost, heuristic(child)))
    return None  # went through everything and never found goal


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # work backwards from end to front
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


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


if __name__ == "__main__":
    maze: Maze = Maze()
    print(maze)
    solution1: Optional[Node[MazeLocation]] = dfs(
        maze.start, maze.goal_test, maze.successors)

    if solution1 is None:
        print("Couldn't find a solution with dfs!")
    else:
        path1: List[MazeLocation] = node_to_path(solution1)
        maze.mark(path1)
        print("dfs solution:")
        print(maze)
        maze.clear(path1)

    solution2: Optional[Node[MazeLocation]] = bfs(
        maze.start, maze.goal_test, maze.successors)

    if solution2 is None:
        print("Couldn't find a solution with bfs!")
    else:
        path2: List[MazeLocation] = node_to_path(solution2)
        maze.mark(path2)
        print("bfs solution:")
        print(maze)
        maze.clear(path2)

    distance: Callable[[MazeLocation], float] = manhattan_distance(maze.goal)
    solution3: Optional[Node[MazeLocation]] = astar(
        maze.start, maze.goal_test, maze.successors, distance)

    if solution3 is None:
        print("Couldn't find a solution with A*!")
    else:
        path3: List[MazeLocation] = node_to_path(solution3)
        maze.mark(path3)
        print("A* solution:")
        print(maze)
