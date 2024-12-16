# https://adventofcode.com/2024/day/7

from parse import parse

sample = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def is_valid1(line):
    total, (arg, *args) = line
    partials = [arg]
    for a in args:
        partials = [x + a for x in partials] + [x * a for x in partials]
    return total in partials


def solve1(input):
    """
    >>> solve1(sample)
    3749
    """
    lines = [
        (m.fixed[0], [int(x) for x in m.fixed[1].split()])
        for s in input.splitlines()
        if (m := parse("{:d}: {}", s))
    ]
    return sum(s[0] for s in lines if is_valid1(s))


def is_valid2(line):
    total, (arg, *args) = line
    partials = [arg]
    for a in args:
        partials = (
            [x + a for x in partials]
            + [x * a for x in partials]
            + [int(str(x) + str(a)) for x in partials]
        )
    return total in partials


def solve2(input):
    """
    >>> solve2(sample)
    11387
    """

    lines = [
        (m.fixed[0], [int(x) for x in m.fixed[1].split()])
        for s in input.splitlines()
        if (m := parse("{:d}: {}", s))
    ]
    return sum(s[0] for s in lines if is_valid2(s))
