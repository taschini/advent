sample = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


def parse_input(input):
    """
    >>> parse_input(sample)
    [('32T3K', 765), ('T55J5', 684), ('KK677', 28), ('KTJJT', 220), ('QQQJA', 483)]
    """
    return [
        (hand, int(bid)) for line in input.splitlines() for hand, bid in [line.split()]
    ]


hand_ranks = [[1, 1, 1, 1, 1], [2, 1, 1, 1], [2, 2, 1], [3, 1, 1], [3, 2], [4, 1], [5]]


def rank(hand):
    """
    >>> [rank(h) for h in ["AAAAA", "AAAAK", "AAAKK", "AAAKQ", "AAKKQ", "AAKQT", "AKQT9"]]
    [6, 5, 4, 3, 2, 1, 0]
    """
    from collections import Counter

    return hand_ranks.index([v for k, v in Counter(hand).most_common()])


def solve1(
    input,
    rank_function=rank,
    card_ranks=["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"],
):
    """
    >>> solve1(sample)
    6440
    """
    return sum(
        r * bid
        for r, (_, bid) in enumerate(
            sorted(
                ([rank_function(hand)] + [card_ranks.index(c) for c in hand], bid)
                for hand, bid in parse_input(input)
            ),
            1,
        )
    )


def rank_with_joker(hand):
    """
    >>> [rank_with_joker(h) for h in ["JJJJJ", "AAAKJ"]]
    [6, 5]
    """
    from collections import Counter

    if hand == "JJJJJ":
        return len(hand_ranks) - 1
    else:
        joker_value = Counter(hand.replace("J", "")).most_common(1)[0][0]
        return rank(hand.replace("J", joker_value))


def solve2(input):
    """
    >>> solve2(sample)
    5905
    """
    return solve1(
        input,
        rank_with_joker,
        ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"],
    )
