# https://adventofcode.com/2024/day/2

sample = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def valid(r: list[int], skip: int) -> bool:
    delta = [r[i + 1] - r[i] for i in range(len(r) - 1)]
    y = all(1 <= d <= 3 for d in delta) or all(-3 <= d <= -1 for d in delta)
    if y or skip == 0:
        return y
    return any(valid(r[:i] + r[i + 1 :], skip - 1) for i in range(len(r)))


def solve1(input):
    """
    >>> solve1(sample)
    2
    """
    return sum(
        1 if valid([int(x) for x in s.split()], skip=0) else 0
        for s in input.splitlines()
    )


def solve2(input):
    """
    >>> solve2(sample)
    4
    """
    return sum(
        1 if valid([int(x) for x in s.split()], skip=1) else 0
        for s in input.splitlines()
    )
