sample = """\
Time:      7  15   30
Distance:  9  40  200
"""


def count_ways(t, d):
    """
    >>> count_ways(7, 9)
    4
    """
    import math

    delta = t**2 - 4 * d
    return (
        0
        if delta < 0
        else math.ceil((t + math.sqrt(delta)) / 2 - 1)
        - math.floor((t - math.sqrt(delta)) / 2 + 1)
        + 1
    )


def solve1(input):
    """
    >>> solve1(sample)
    288
    """
    import math

    ts, ds = [
        [int(x) for x in line.split(":")[1].split()] for line in input.splitlines()
    ]

    ways = [count_ways(t, d) for t, d in zip(ts, ds)]
    return math.prod(ways)


def solve2(input):
    """
    >>> solve2(sample)
    71503
    """
    t, d = [int("".join(line.split(":")[1].split())) for line in input.splitlines()]
    return count_ways(t, d)
