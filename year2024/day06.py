# https://adventofcode.com/2024/day/6

from collections import abc
from typing import NamedTuple

sample = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
MAX_ITERATIONS = 1000


def to_next_obstacle(guard, crates) -> int | None:
    """Return the distance to the next obstacle in the direction the guard is facing."""
    gi, gj, gd = guard
    di, dj = directions[gd]

    return min(
        (
            c
            for i, j in crates
            if (c := (i - gi) * di + (j - gj) * dj) > 0
            and (i - gi) * dj == (j - gj) * di
        ),
        default=None,
    )


def to_perimeter(guard, size) -> int:
    """Return the distance to the perimeter in the direction the guard is facing."""
    y = to_next_obstacle(
        guard,
        [
            (guard[0], -1),
            (guard[0], size[1]),
            (-1, guard[1]),
            (size[0], guard[1]),
        ],
    )
    assert y is not None
    return y


def steps_ahead(
    guard, crates, size: tuple[int, int] | None
) -> abc.Generator[tuple[int, int]]:
    """Iterate through the steps the guard can take without changing direction.

    If the guard is leaving the area, the last step returned is None.
    """
    leaving = False
    di, dj = directions[guard[2]]
    nc = to_next_obstacle(guard, crates)
    if nc is None:
        nc = to_perimeter(guard, size) if size is not None else 0
        leaving = True
    for c in range(nc):
        yield (guard[0] + c * di, guard[1] + c * dj)
    if leaving:
        yield None


class Puzzle(NamedTuple):
    crates: set[tuple[int, int]]
    initial: tuple[int, int, int]
    size: tuple[int, int]

    @classmethod
    def parse(cls, input: str):
        crates = set()
        for i, s in enumerate(input.splitlines()):
            for j, c in enumerate(s):
                if c == "^":
                    guard = (i, j, 0)
                elif c == "#":
                    crates.add((i, j))
        return cls(crates=crates, initial=guard, size=(i + 1, j + 1))


def solve1(input):
    """
    >>> solve1(sample)
    41
    """
    p = Puzzle.parse(input)

    visited = set()
    guard = p.initial

    for _ in range(MAX_ITERATIONS):
        for next in steps_ahead(guard, p.crates, p.size):
            if next is None:
                return len(visited)
            visited.add(next)
        guard = next + ((guard[2] + 1) % 4,)
    assert False


def detect_loop(crates, guard, traced=None):
    """
    >>> p = Puzzle.parse(sample)
    >>> detect_loop(p.crates, p.initial)
    False

    >>> detect_loop(p.crates | {(6, 3)}, p.initial)
    True

    """
    traced = traced.copy() if traced is not None else set()
    for _ in range(MAX_ITERATIONS):
        for next in steps_ahead(guard, crates, size=None):
            if next is None:
                return False
            traced.add(next + (guard[2],))
        guard = next + ((guard[2] + 1) % 4,)
        if guard in traced:
            return True
    assert False


def solve2(input):
    """
    >>> solve2(sample)
    6
    """
    p = Puzzle.parse(input)

    visited = set()
    traced = set()
    loop_makers = set()
    initial = guard = p.initial

    for _ in range(MAX_ITERATIONS):
        for next in steps_ahead(guard, p.crates, p.size):
            if next is None:
                return len(loop_makers - {initial[:2]})
            if next not in visited and detect_loop(p.crates | {next}, guard, traced):
                loop_makers.add(next)
            visited.add(next)
            guard = next + (guard[2],)
            traced.add(guard)
        guard = next + ((guard[2] + 1) % 4,)
    assert False
