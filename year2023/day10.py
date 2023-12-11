sample1 = """\
.....
.S-7.
.|.|.
.L-J.
.....
"""

sample2 = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

sample3 = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

sample4 = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

sample5 = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""


pipes = {
    "J": [(0, -1), (-1, 0)],
    "L": [(-1, 0), (0, +1)],
    "F": [(+1, 0), (0, +1)],
    "7": [(+1, 0), (0, -1)],
    "-": [(0, -1), (0, +1)],
    "|": [(-1, 0), (+1, 0)],
}


def solve1(input):
    """
    >>> solve1(sample1)
    4

    >>> solve1(sample2)
    8

    """
    graph = parse_input(input)
    _, k = find_main_loop(graph)
    return k


def find_main_loop(graph):
    from itertools import count

    start = list(graph)[-1]
    mainloop = {start}
    current = {start}
    for k in count():
        current = {n for v in current for n in graph[v] if n not in mainloop}
        if not current:
            break
        mainloop |= current
    return mainloop, k


def parse_input(input):
    graph = {}
    start = None
    for i, line in enumerate(input.splitlines()):
        for j, c in enumerate(line):
            if c == ".":
                pass
            elif c == "S":
                start = (i, j)
            else:
                graph[(i, j)] = [(i + p, j + q) for p, q in pipes[c]]

    graph[start] = [n for n, cs in graph.items() if start in cs]
    assert len(graph[start]) == 2
    return graph


def solve2(input):
    """
    >>> solve2(sample1)
    1

    >>> solve2(sample2)
    1

    >>> solve2(sample3)
    4

    >>> solve2(sample4)
    8

    >>> solve2(sample5)
    10

    """
    graph = parse_input(input)
    loop, _ = find_main_loop(graph)
    inside = 0

    for i, line in enumerate(input.splitlines()):
        cross_up = 0
        cross_dn = 0
        for j, _ in enumerate(line):
            if (i, j) in loop:
                cross_up += int(any(p < i for p, _ in graph[i, j]))
                cross_dn += int(any(p > i for p, _ in graph[i, j]))
            else:
                if (cross_up % 2) and (cross_dn % 2):
                    inside += 1
    return inside
