# https://adventofcode.com/2024/day/10

import numpy as np

sample = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse(input):
    grid = np.array([[int(c) for c in s] for s in input.splitlines()])
    r, c = grid.shape
    trailheads = [(i, j) for i in range(r) for j in range(c) if grid[i, j] == 0]
    return grid, trailheads


def solve1(input):
    """
    >>> solve1(sample)
    36
    """
    grid, trailheads = parse(input)

    total = 0
    for h in trailheads:
        front = {h}
        peaks = set()
        while front:
            front = {
                (xi, xj)
                for i, j in front
                for di, dj in directions
                if 0 <= (xi := i + di) < grid.shape[0]
                and 0 <= (xj := j + dj) < grid.shape[1]
                and grid[xi, xj] == grid[i, j] + 1
            }
            peaks.update((i, j) for i, j in front if grid[i, j] == 9)
        total += len(peaks)
    return total


def solve2(input):
    """
    >>> solve2(sample)
    81
    """
    grid, trailheads = parse(input)

    total = 0
    for h in trailheads:
        stack = [h]
        rating = 0
        while stack:
            (i, j) = stack.pop()
            if grid[i, j] == 9:
                rating += 1
            stack.extend(
                (xi, xj)
                for di, dj in directions
                if 0 <= (xi := i + di) < grid.shape[0]
                and 0 <= (xj := j + dj) < grid.shape[1]
                and grid[xi, xj] == grid[i, j] + 1
            )
        total += rating
    return total
