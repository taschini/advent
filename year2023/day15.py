# https://adventofcode.com/2023/day/15

sample = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""


def hash(s):
    """
    >>> hash("HASH")
    52
    """
    x = 0
    for c in s:
        x = (x + ord(c)) * 17 % 256
    return x


def solve1(input):
    """
    >>> solve1(sample)
    1320
    """
    return sum(hash(s) for s in input.replace("\n", "").split(","))


def solve2(input):
    """
    >>> solve2(sample)
    145
    """
    import re
    from collections import defaultdict

    regex = re.compile("(.*)(=|-)(.*)?")
    data = [regex.match(s).groups() for s in input.replace("\n", "").split(",")]

    boxes = defaultdict(dict)
    for label, op, f in data:
        box = hash(label)
        if op == "=":
            boxes[box][label] = int(f)
        else:
            boxes[box].pop(label, None)

    return sum(
        ((1 + box) * (slot + 1) * f)
        for box, lenses in boxes.items()
        for slot, f in enumerate(lenses.values())
    )
