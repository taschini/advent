# https://adventofcode.com/2023/day/18

sample = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""


def compute_discrete_area(movements: list[tuple[tuple[int, int], int]]):
    from more_itertools import pairwise

    vertices = [(0, 0)]
    for direction, distance in movements:
        vertices.append(
            tuple(x + y * distance for x, y in zip(vertices[-1], direction))
        )

    area = abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in pairwise(vertices))) // 2
    perimeter = sum(
        abs(x2 - x1) + abs(y2 - y1) for (x1, y1), (x2, y2) in pairwise(vertices)
    )

    return area + perimeter // 2 + 1


directions = {"R": (0, +1), "D": (+1, 0), "L": (0, -1), "U": (-1, 0)}


def solve1(input):
    """
    >>> solve1(sample)
    62
    """
    from parse import parse

    return compute_discrete_area(
        (directions[d], l)
        for d, l, _ in [parse("{} {:d} (#{})", s).fixed for s in input.splitlines()]
    )


def solve2(input):
    """
    >>> solve2(sample)
    952408144115
    """
    from parse import parse

    dirs = list(directions.values())
    return compute_discrete_area(
        (dirs[d], l)
        for _, l, d in [parse("{} (#{:5x}{:d})", s).fixed for s in input.splitlines()]
    )
