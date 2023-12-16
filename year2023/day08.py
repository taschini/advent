# https://adventofcode.com/2023/day/8

sample1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

sample2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

sample3 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


def parse_input(input):
    """
    >>> parse_input(sample2)  # doctest: +NORMALIZE_WHITESPACE
    ('LLR',
     {'AAA': {'L': 'BBB', 'R': 'BBB'},
      'BBB': {'L': 'AAA', 'R': 'ZZZ'},
      'ZZZ': {'L': 'ZZZ', 'R': 'ZZZ'}})

    """
    from parse import parse

    path, nodes = input.split("\n\n")
    return path, {
        n: {"L": l, "R": r}
        for line in nodes.splitlines()
        for n, l, r in [parse("{} = ({}, {})", line).fixed]
    }


def solve1(input):
    """
    >>> solve1(sample1)
    2

    >>> solve1(sample2)
    6
    """
    from itertools import cycle

    path, graph = parse_input(input)
    node = "AAA"

    for n, c in enumerate(cycle(path), 1):
        node = graph[node][c]
        if node == "ZZZ":
            break

    return n


def solve2(input):
    """
    >>> solve2(sample3)
    6
    """
    import math
    from itertools import cycle

    path, graph = parse_input(input)

    times = []
    for node in [n for n in graph if n.endswith("A")]:
        for n, c in enumerate(cycle(path), 1):
            node = graph[node][c]
            if node.endswith("Z"):
                break
        times.append(n)

    return math.lcm(*times)
