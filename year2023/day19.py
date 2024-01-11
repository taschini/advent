# https://adventofcode.com/2023/day/19

from collections import namedtuple

sample = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


def solve1(input):
    """
    >>> solve1(sample)
    19114
    """
    from parse import parse

    def always_true(x, m, a, s):
        return True

    def parse_condition(condition):
        return eval(f"lambda x, m, a, s: {condition}")

    workflows, ratings = input.split("\n\n")

    ratings = [
        eval(f"dict({parse('{{{}}}', s).fixed[0]})") for s in ratings.splitlines()
    ]

    workflows = {
        n: [
            (parse_condition(ps[0]), ps[1])
            if len(ps := r.split(":")) == 2
            else (always_true, ps[0])
            for r in rs.split(",")
        ]
        for n, rs in [parse("{}{{{}}}", s).fixed for s in workflows.splitlines()]
    }

    tot = 0
    for part in ratings:
        name = "in"
        while name not in ("R", "A"):
            for condition, next in workflows[name]:
                if condition(**part):
                    name = next
                    break
            else:
                assert False
        if name == "A":
            tot += sum(part.values())

    return tot


def solve2(input):
    """
    >>> solve2(sample)
    167409079868000
    """
    import math

    from parse import parse

    workflows, _ = input.split("\n\n")
    full_range = Interval(1, 4000)
    parts = [(Part(x=full_range, m=full_range, a=full_range, s=full_range), "in")]

    def parse_rule(condition, target=None):
        if target is None:
            return (None, None, condition)
        var, op, threshold = parse("{1}{1}{:d}", condition).fixed

        return (
            var,
            Interval(1, threshold - 1) if op == "<" else Interval(threshold + 1, 4000),
            target,
        )

    workflows = {
        n: [parse_rule(*r.split(":")) for r in rs.split(",")]
        for n, rs in [parse("{}{{{}}}", s).fixed for s in workflows.splitlines()]
    }

    accepted = []
    while parts:
        part, name = parts.pop()
        if name == "A":
            accepted.append(part)
            continue
        if name == "R":
            continue
        for var, mask, target in workflows[name]:
            if var is None:
                parts.append((part, target))
                continue
            current = getattr(part, var)
            if (next := current & mask).empty:
                continue
            parts.append((part.replace(var, next), target))
            for interval in current - next:
                parts.append((part.replace(var, interval), name))
            break

    return sum(math.prod(sup - inf + 1 for inf, sup in p) for p in accepted)


class Part(namedtuple("Part", "x m a s")):
    __slots__ = ()

    def replace(self, var, value):
        return self._replace(**{var: value})


class Interval(namedtuple("Interval", "inf sup")):
    """Discrete closed intervals."""

    __slots__ = ()

    @property
    def empty(self) -> bool:
        """
        >>> Interval(0, 1).empty
        False

        >>> Interval(1, 0).empty
        True
        """
        return self.inf > self.sup

    def __and__(self, other: "Interval") -> "Interval":
        """
        >>> Interval(1, 3) & Interval(2, 4)
        Interval(inf=2, sup=3)
        """
        return type(self)(max(self.inf, other.inf), min(self.sup, other.sup))

    def __sub__(self, other: "Interval") -> list["Interval"]:
        """
        >>> Interval(0, 5) - Interval(2, 3)
        [Interval(inf=0, sup=1), Interval(inf=4, sup=5)]
        """
        result = []
        if self.inf < other.inf < self.sup:
            result.append(Interval(self.inf, other.inf - 1))
        if self.inf < other.sup < self.sup:
            result.append(Interval(other.sup + 1, self.sup))
        return result
