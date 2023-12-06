sample = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def solve1(input):
    """
    >>> solve1(sample)
    4361
    """
    adjacent = set()
    numbers = []
    current_value = 0
    current_position = set()
    for i, line in enumerate(input.splitlines()):
        for j, c in enumerate(line + "."):
            if c.isnumeric():
                current_value = current_value * 10 + int(c)
                current_position.add((i, j))
                continue
            if current_value != 0:
                numbers.append((current_value, current_position))
                current_value = 0
                current_position = set()
            if c != ".":
                adjacent |= {
                    (i + p, j + q) for p in [-1, 0, 1] for q in [-1, 0, 1] if p or q
                }

    return sum(n for n, p in numbers if p & adjacent)


def solve2(input):
    """
    >>> solve2(sample)
    467835
    """
    import math

    adjacent = []
    numbers = []
    current_value = 0
    current_position = set()
    for i, line in enumerate(input.splitlines()):
        for j, c in enumerate(line + "."):
            if c.isnumeric():
                current_value = current_value * 10 + int(c)
                current_position.add((i, j))
                continue
            if current_value != 0:
                numbers.append((current_value, current_position))
                current_value = 0
                current_position = set()
            if c == "*":
                adjacent.append(
                    {(i + p, j + q) for p in [-1, 0, 1] for q in [-1, 0, 1] if p or q}
                )

    return sum(
        math.prod(x)
        for c in adjacent
        if len(x := [n for n, p in numbers if p & c]) == 2
    )
