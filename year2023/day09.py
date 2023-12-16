# https://adventofcode.com/2023/day/9

sample = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def solve1(input):
    """
    >>> solve1(sample)
    114
    """
    import pandas as pd

    tot = 0
    for series in [pd.Series(map(int, line.split())) for line in input.splitlines()]:
        latest = []
        while series.abs().max() > 0:
            latest.append(series.iloc[-1])
            series = series.diff().dropna()
        tot += sum(latest)

    return int(tot)


def solve2(input):
    """
    >>> solve2(sample)
    2
    """
    import pandas as pd

    tot = 0
    for series in [pd.Series(map(int, line.split())) for line in input.splitlines()]:
        earliest = []
        while series.abs().max() > 0:
            earliest.append(series.iloc[0])
            series = series.diff().dropna()
        extra = 0
        for x in reversed(earliest):
            extra = x - extra
        tot += extra

    return int(tot)
