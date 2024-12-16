# https://adventofcode.com/2024/day/8

from itertools import count, permutations

sample = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


def parse(input):
    antennas = {}
    for i, s in enumerate(input.splitlines()):
        for j, c in enumerate(s):
            if c != ".":
                antennas.setdefault(c, []).append((i, j))
    return i + 1, j + 1, antennas


def solve1(input):
    """
    >>> solve1(sample)
    14
    """
    rows, cols, antennas = parse(input)

    antinodes = {
        (xi, xj)
        for k in antennas.values()
        for (ai, aj), (bi, bj) in permutations(k, 2)
        if 0 <= (xi := 2 * ai - bi) < rows and 0 <= (xj := 2 * aj - bj) < cols
    }
    return len(antinodes)


def solve2(input):
    """
    >>> solve2(sample)
    34
    """
    rows, cols, antennas = parse(input)

    antinodes = set()
    for k in antennas.values():
        for (ai, aj), (bi, bj) in permutations(k, 2):
            for c in count():
                xi, xj = (ai - c * (bi - ai), aj - c * (bj - aj))
                if not (0 <= xi < rows and 0 <= xj < cols):
                    break
                antinodes.add((xi, xj))

    return len(antinodes)
