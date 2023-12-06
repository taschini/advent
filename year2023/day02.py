sample = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def parse_game(input):
    from parse import parse

    return {
        match["game"]: [
            {
                m["color"]: m["count"]
                for e in draw.split(", ")
                if (m := parse("{count:d} {color}", e))
            }
            for draw in match["draws"].split("; ")
        ]
        for line in input.splitlines()
        if (match := parse("Game {game:d}: {draws}", line))
    }


def solve1(input):
    """
    >>> solve1(sample)
    8
    """
    limits = {"red": 12, "green": 13, "blue": 14}
    return sum(
        i
        for i, g in parse_game(input).items()
        if all(d.get(c, 0) <= m for c, m in limits.items() for d in g)
    )


def solve2(input):
    """
    >>> solve2(sample)
    2286
    """
    import math

    return sum(
        math.prod(max(d.get(c, 0) for d in g) for c in ["red", "green", "blue"])
        for g in parse_game(input).values()
    )
