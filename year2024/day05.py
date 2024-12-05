# https://adventofcode.com/2024/day/5

from graphlib import TopologicalSorter
from typing import NamedTuple, Self

from parse import parse

sample = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


class Puzzle(NamedTuple):
    rules: list[tuple[int, int]]
    batches: list[list[int]]

    @classmethod
    def parse(cls, input: str) -> Self:
        lines = input.splitlines()
        return cls(
            rules=[m.fixed for s in lines if (m := parse("{:d}|{:d}", s)) is not None],
            batches=[[int(x) for x in s.split(",")] for s in lines if "," in s],
        )

    def is_valid(self, batch):
        return all(
            batch.index(x) < batch.index(y)
            for x, y in self.rules
            if x in batch and y in batch
        )

    def sort(self, batch):
        graph = {}
        for x, y in self.rules:
            if x in batch and y in batch:
                graph.setdefault(y, set()).add(x)
        return list(TopologicalSorter(graph).static_order())


def solve1(input):
    """
    >>> solve1(sample)
    143
    """
    p = Puzzle.parse(input)
    return sum(b[len(b) // 2] for b in p.batches if p.is_valid(b))


def solve2(input):
    """
    >>> solve2(sample)
    123
    """
    p = Puzzle.parse(input)
    return sum(p.sort(b)[len(b) // 2] for b in p.batches if not p.is_valid(b))
