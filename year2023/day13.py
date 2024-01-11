# https://adventofcode.com/2023/day/13

sample = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


def find_reflections(pattern, tolerance=0):
    lines = pattern.splitlines()
    rows = len(lines)
    cols = len(lines[0])
    coords = [(i, j) for i, s in enumerate(lines) for j, c in enumerate(s) if c == "#"]
    reflections = []
    for k in range(1, cols):
        clipped = {(i, j) for i, j in coords if 0 <= 2 * k - j - 1 < cols}
        reflected = {(i, 2 * k - j - 1) for i, j in clipped}
        if len(clipped ^ reflected) == tolerance * 2:
            reflections.append(k)
    for h in range(1, rows):
        clipped = {(i, j) for i, j in coords if 0 <= 2 * h - i - 1 < rows}
        reflected = {(2 * h - i - 1, j) for i, j in clipped}
        if len(clipped ^ reflected) == tolerance * 2:
            reflections.append(100 * h)
    return reflections


def solve1(input):
    """
    >>> solve1(sample)
    405
    """
    return sum(x for p in input.split("\n\n") for x in find_reflections(p))


def solve2(input):
    """
    >>> solve2(sample)
    400
    """
    return sum(x for p in input.split("\n\n") for x in find_reflections(p, tolerance=1))
