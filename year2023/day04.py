# https://adventofcode.com/2023/day/4

sample = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def score_cards(input):
    """
    >>> score_cards(sample)
    [4, 2, 2, 1, 0, 0]
    """
    from parse import parse

    return [
        len(set(match["winners"].split()) & set(match["draws"].split()))
        for line in input.splitlines()
        if (match := parse("Card {card}: {winners} | {draws}", line))
    ]


def solve1(input):
    """
    >>> solve1(sample)
    13
    """
    return sum(2 ** (score - 1) for score in score_cards(input) if score)


def solve2(input):
    """
    >>> solve2(sample)
    30
    """
    scores = score_cards(input)

    multiples = [1 for _ in scores]
    for i, s in enumerate(scores):
        for j in range(i + 1, i + s + 1):
            multiples[j] += multiples[i]
    return sum(multiples)
