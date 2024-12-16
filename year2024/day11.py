# https://adventofcode.com/2024/day/11


from collections import Counter


def transform(s: int) -> list[int]:
    if s == 0:
        return [1]
    t = str(s)
    if len(t) % 2 == 0:
        k = len(t) // 2
        return [int(t[:k]), int(t[k:])]
    return [s * 2024]


def blink(stones: Counter[int]) -> Counter[int]:
    """
    >>> blink(Counter([0, 1, 10, 99, 999]))
    Counter({1: 2, 9: 2, 2024: 1, 0: 1, 2021976: 1})
    """
    z = Counter()
    for s, c in stones.items():
        for x in transform(s):
            z[x] += c
    return z


def solve(input: str, n: int) -> int:
    """
    >>> solve("125 17", 6)
    22
    """
    stones = Counter(int(x) for x in input.split())
    for _ in range(n):
        stones = blink(stones)
    return stones.total()


def solve1(input):
    """
    >>> solve1("125 17")
    55312
    """
    return solve(input, 25)


def solve2(input):
    return solve(input, 75)
