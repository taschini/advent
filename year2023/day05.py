# https://adventofcode.com/2023/day/5

sample = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def parse_input(input):
    """
    >>> parse_input(sample)  # doctest: +NORMALIZE_WHITESPACE
    [[[79, 14, 55, 13]],
     [[50, 98, 2], [52, 50, 48]],
     [[0, 15, 37], [37, 52, 2], [39, 0, 15]],
     [[49, 53, 8], [0, 11, 42], [42, 0, 7], [57, 7, 4]],
     [[88, 18, 7], [18, 25, 70]],
     [[45, 77, 23], [81, 45, 19], [68, 64, 13]],
     [[0, 69, 1], [1, 0, 69]], [[60, 56, 37], [56, 93, 4]]]
    """
    from parse import parse

    return [
        [[int(x) for x in line.split()] for line in match["body"].strip().splitlines()]
        for section in input.split("\n\n")
        if (match := parse("{heading}:{body}", section))
    ]


def apply(map: list[list[int]], x: int) -> int:
    """
    >>> apply([[50, 98, 2], [52, 50, 48]], 57)
    59

    >>> apply([[50, 98, 2], [52, 50, 48]], 30)
    30
    """
    for target, source, length in map:
        if 0 <= (d := x - source) < length:
            return target + d
    return x


def solve1(input):
    """
    >>> solve1(sample)
    35
    """
    [points], *maps = parse_input(input)

    for map in maps:
        points = [apply(map, s) for s in points]

    return min(points)


def complete(intervals):
    """Complete a list of closed-open intervals to cover all integer numbers.

    >>> complete([(1, 3), (4, 6)])
    [(-inf, 1), (1, 3), (3, 4), (4, 6), (6, inf)]
    """
    import numpy as np
    from more_itertools import flatten, pairwise

    return list(pairwise([-np.inf] + sorted(set(flatten(intervals))) + [np.inf]))


def solve2(input):
    """
    >>> solve2(sample)
    46
    """
    from more_itertools import chunked

    [seeds], *maps = parse_input(input)

    # Closed-open intervals
    intervals = sorted((x, x + r) for x, r in chunked(seeds, 2))
    for map in maps:
        intervals = sorted(
            (apply(map, x), apply(map, y - 1) + 1)  # (map(x), lim(x->y-) map(x))
            for p, q in intervals
            for r, s in complete((s, s + r) for _, s, r in map)
            if (x := max(p, r)) < (y := min(q, s))
        )

    return intervals[0][0]
