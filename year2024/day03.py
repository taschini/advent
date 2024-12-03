# https://adventofcode.com/2024/day/3

import math
import re

sample1 = """\
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

sample2 = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""


def solve1(input):
    """
    >>> solve1(sample1)
    161
    """
    return sum(
        math.prod([int(x) for x in s]) for s in re.findall(r"mul\((\d+),(\d+)\)", input)
    )


def solve2(input):
    """
    >>> solve2(sample2)
    48
    """

    commands = [
        [x for x in s if x]
        for s in re.findall(
            r"(?:(mul)\((\d+),(\d+)\))|(?:(do)\(\))|(?:(don't)\(\))", input
        )
    ]
    total = 0
    active = True
    for s in commands:
        match s:
            case ["mul", a, b]:
                if active:
                    total += int(a) * int(b)
            case ["do"]:
                active = True
            case ["don't"]:
                active = False
    return total
