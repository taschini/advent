# https://adventofcode.com/2024/day/4

import re

import numpy as np

sample = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def solve1(input):
    """
    >>> solve1(sample)
    18
    """
    matrix = np.array([list(s) for s in input.splitlines()])
    assert matrix.shape[0] == matrix.shape[1]

    return sum(
        len(re.findall("XMAS", s))
        for orientation in [
            np.apply_along_axis("".join, axis=1, arr=matrix),
            np.apply_along_axis("".join, axis=0, arr=matrix),
            diagonals(matrix),
            diagonals(matrix[::-1, :]),
        ]
        for row in orientation
        for s in [row, row[::-1]]
    )


def solve2(input):
    """
    >>> solve2(sample)
    9
    """
    matrix = np.array([list(s) for s in input.splitlines()])
    assert matrix.shape[0] == matrix.shape[1]
    size = len(matrix)

    m1 = {
        (
            max(size - y - 1, 0) + m.start() + 1,
            max(y - size + 1, 0) + m.start() + 1,
        )
        for y, s in enumerate(diagonals(matrix))
        for p in ["SAM", "MAS"]
        for m in re.finditer(p, s)
    }

    m2 = {
        (
            size - 1 - (max(size - y - 1, 0) + m.start() + 1),
            max(y - size + 1, 0) + m.start() + 1,
        )
        for y, s in enumerate(diagonals(matrix[::-1, :]))
        for p in ["SAM", "MAS"]
        for m in re.finditer(p, s)
    }

    return len(m1 & m2)


def diagonals(matrix):
    size = len(matrix)
    return ["".join(matrix.diagonal(i)) for i in range(-size + 1, size)]
