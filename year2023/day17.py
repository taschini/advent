# https://adventofcode.com/2023/day/17

from collections import namedtuple

sample = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

Node = namedtuple("Node", "i j dir streak")


def find_distance(input, min_streak, max_streak):
    from heapq import heappop, heappush

    from more_itertools import one

    grid = [[int(c) for c in s] for s in input.splitlines()]
    rows = len(grid)
    cols = one({len(r) for r in grid})
    visited = {}
    scheduled = set()
    queue = [(0, Node(i=0, j=0, dir=None, streak=0))]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    minimum = float("inf")
    while queue:
        cost, node = heappop(queue)
        if node in visited:
            continue
        visited[node] = cost
        if cost >= minimum:
            continue
        if node.i == rows - 1 and node.j == cols - 1:
            minimum = min(minimum, cost)
        candidates = [
            Node(i, j, dir, streak=streak)
            for dir, (di, dj) in enumerate(directions)
            if 0 <= (i := node.i + di) < rows
            and 0 <= (j := node.j + dj) < cols
            and node.dir != (dir + 2) % 4  # No reverse direction
            and (streak := node.streak + 1 if dir == node.dir else 1) <= max_streak
            and (node.dir is None or node.dir == dir or node.streak >= min_streak)
        ]
        for c in candidates:
            if c not in scheduled and (new_cost := cost + grid[c.i][c.j]) < minimum:
                scheduled.add(c)
                heappush(queue, (new_cost, c))

    return minimum


def solve1(input):
    """
    >>> solve1(sample)
    102
    """
    return find_distance(input, min_streak=1, max_streak=3)


def solve2(input):
    """
    >>> solve2(sample)
    94
    """
    return find_distance(input, min_streak=4, max_streak=10)
