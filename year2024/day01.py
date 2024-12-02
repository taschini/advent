# https://adventofcode.com/2024/day/1

import io

import pandas as pd

sample = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""


def parse(input):
    return pd.read_csv(
        io.StringIO(input),
        sep=r"\s+",
        header=None,
        names=["left", "right"],
    )


def solve1(input):
    """
    >>> solve1(sample)
    11
    """
    df = parse(input).apply(sorted, axis=0)
    return int((df.left - df.right).abs().sum())


def solve2(input):
    """
    >>> solve2(sample)
    31
    """
    df = parse(input)
    c = df.right.value_counts()
    return int(sum(x * c.get(x, 0) for x in df.left))
