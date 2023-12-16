# https://adventofcode.com/2023/day/1

sample1 = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""


def solve1(input):
    """
    >>> solve1(sample1)
    142
    """
    return sum(
        int(d[0] + d[-1])
        for s in input.splitlines()
        if (d := [c for c in s if c.isnumeric()])
    )


sample2 = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


def solve2(input):
    """
    >>> solve2(sample2)
    281
    """

    digits = {
        d: str(i)
        for i, d in enumerate(
            ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"], 1
        )
    } | {str(i): str(i) for i in range(1, 10)}

    return sum(
        int(d[0] + d[-1])
        for s in input.splitlines()
        if (
            d := [
                v
                for i in range(len(s))
                for k, v in digits.items()
                if s[i:].startswith(k)
            ]
        )
    )
