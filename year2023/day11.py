# https://adventofcode.com/2023/day/11

sample = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


def distance(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def compute_offsets(size, occupied):
    import pandas as pd

    return pd.Series(int(i not in occupied) for i in range(size)).cumsum()


def find_galaxies(input, factor):
    lines = input.splitlines()
    coords = [
        (i, j) for i, line in enumerate(lines) for j, c in enumerate(line) if c == "#"
    ]

    row_offsets = compute_offsets(len(lines), set(i for i, _ in coords)) * factor
    col_offsets = compute_offsets(len(lines[0]), set(j for _, j in coords)) * factor

    return [(i + row_offsets[i], j + col_offsets[j]) for i, j in coords]


def solve1(input, expansion=2):
    """
    >>> solve1(sample)
    374

    >>> solve1(sample, expansion=10)
    1030

    >>> solve1(sample, expansion=100)
    8410

    """
    from itertools import combinations

    return sum(
        distance(x, y) for x, y in combinations(find_galaxies(input, expansion - 1), 2)
    )


def solve2(input):
    return solve1(input, expansion=1000000)
