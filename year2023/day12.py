# https://adventofcode.com/2023/day/12

from functools import cache

sample = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def parse_input(input, repeat=1):
    """
    >>> parse_input(sample)  # doctest: +ELLIPSIS
    [('???.###', (1, 1, 3)), ...]

    >>> parse_input(sample, repeat=2)  # doctest: +ELLIPSIS
    [('???.###????.###', (1, 1, 3, 1, 1, 3)), ...]
    """
    return [
        (
            ("?".join([row] * repeat)).strip("."),
            tuple(map(int, runs.split(","))) * repeat,
        )
        for line in input.splitlines()
        for row, runs in [line.split()]
    ]


@cache
def count_ways(row: str, runs: tuple[int, ...], streak: bool = False):
    r = runs[0] if runs else 0
    if not row:
        return 0 if len(runs) > 1 or r else 1
    c = row[0]
    rest = row.lstrip(c)
    n = len(row) - len(rest)
    if c == "#":
        return 0 if n > r else count_ways(rest, (r - n,) + runs[1:], True)
    if c == ".":
        if streak:
            return 0 if r else count_ways(rest, runs[1:], False)
        return count_ways(rest, runs, False)
    if r > 0:
        s = min(n, r)
        a = count_ways(row[s:], (r - s,) + runs[1:], True)
    else:
        a = 0
    b = count_ways("." + row[1:], runs, streak)
    return a + b


def solve1(input, repeat=1):
    """
    >>> solve1(sample)
    21
    """
    return sum(count_ways(row, runs) for row, runs in parse_input(input, repeat))


def solve2(input):
    """
    >>> solve2(sample)
    525152
    """
    return solve1(input, repeat=5)
