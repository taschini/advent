# https://adventofcode.com/2024/day/9

from typing import TypeAlias

sample = """\
2333133121414131402
"""


LRE: TypeAlias = list[tuple[int | None, int]]


def parse(input: str) -> LRE:
    return [
        (i // 2 if i % 2 == 0 else None, k)
        for i, c in enumerate(input.strip())
        if (k := int(c)) > 0
    ]


def decode(lre: LRE) -> list[int | None]:
    return sum(([i] * c for i, c in lre), [])


def solve1(input):
    """
    >>> solve1(sample)
    1928
    """
    disk = decode(parse(input))

    i = 0
    j = len(disk) - 1
    while i < j:
        while disk[i] is not None and i < j:
            i += 1
        while disk[j] is None and i < j:
            j -= 1
        if disk[i] is None and disk[j] is not None:
            disk[i], disk[j] = disk[j], disk[i]
            i += 1
            j -= 1

    return sum(i * x for i, x in enumerate(disk) if x is not None)


def solve2(input):
    """
    >>> solve2(sample)
    2858
    """
    disk = parse(input)

    j = len(disk) - 1
    while j >= 0:
        if disk[j][0] is not None:
            for i in range(j):
                if disk[i][0] is None and (k := disk[i][1]) >= (h := disk[j][1]):
                    if k > h:
                        disk[i] = (None, h)
                        disk.insert(i + 1, (None, k - h))
                        j += 1
                    disk[i], disk[j] = disk[j], disk[i]
                    break
        j -= 1

    return sum(i * x for i, x in enumerate(decode(disk)) if x is not None)
