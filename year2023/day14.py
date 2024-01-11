# https://adventofcode.com/2023/day/14

from collections import namedtuple

sample = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


class Grid(namedtuple("Grid", "rows cols coords")):
    __slots__ = ()

    @classmethod
    def parse(cls, input: str) -> "Grid":
        """
        >>> Grid.parse(sample)  # doctest: +ELLIPSIS
        Grid(rows=10, cols=10, coords=((0, 0, 'O'), (0, 5, '#'), (1, 0, 'O'), ...))
        """
        lines = input.splitlines()
        return cls(
            rows=len(lines),
            cols=len(lines[0]),
            coords=tuple(
                [
                    (i, j, c)
                    for i, s in enumerate(lines)
                    for j, c in enumerate(s)
                    if c != "."
                ]
            ),
        )

    def render(self) -> str:
        """
        >>> Grid.parse(sample).render() == sample.strip()
        True
        """
        raster = [["."] * self.cols for _ in range(self.rows)]
        for i, j, c in self.coords:
            assert raster[i][j] == "."
            raster[i][j] = c
        return "\n".join("".join(s) for s in raster)

    def tilt(self) -> "Grid":
        """
        >>> print(Grid.parse(sample).tilt().render())
        OOOO.#.O..
        OO..#....#
        OO..O##..O
        O..#.OO...
        ........#.
        ..#....#.#
        ..O..#.O.O
        ..O.......
        #....###..
        #....#....
        """
        from collections import defaultdict
        from itertools import pairwise

        walls = [[-1] for _ in range(self.cols)]
        for i, j, c in self.coords:
            if c == "#":
                walls[j].append(i)
        walls = [sorted(col) + [self.rows] for col in walls]

        supports = [
            [x + 1 for x, y in pairwise(col) for _ in range(x, y)] for col in walls
        ]

        balls = [defaultdict(int) for _ in range(self.cols)]
        for i, j, c in self.coords:
            if c == "O":
                balls[j][supports[j][i]] += 1

        return type(self)(
            rows=self.rows,
            cols=self.cols,
            coords=tuple(
                [
                    (k, j, "O")
                    for j, d in enumerate(balls)
                    for i, n in d.items()
                    for k in range(i, i + n)
                ]
                + [(i, j, "#") for j, col in enumerate(walls) for i in col[1:-1]]
            ),
        )

    def get_load(self):
        """
        >>> Grid.parse(sample).tilt().get_load()
        136
        """
        return sum(self.rows - i for i, _, c in self.coords if c == "O")

    def rotate(self):
        """
        >>> print(Grid.parse(sample).rotate().render())
        ##..O.O.OO
        O....OO...
        O..O#...O.
        ......#.O.
        ......O.#.
        ##.#O..#.#
        .#.O...#..
        .#O.#O....
        .....#....
        ...O#.O.#.
        """
        return type(self)(
            rows=self.rows,
            cols=self.cols,
            coords=tuple([(j, self.rows - i - 1, c) for i, j, c in self.coords]),
        )

    def spin(self):
        """
        >>> print("-"); print(Grid.parse(sample).spin().render())
        -
        .....#....
        ....#...O#
        ...OO##...
        .OO#......
        .....OOO#.
        .O#...O#.#
        ....O#....
        ......OOOO
        #...O###..
        #..OO#....
        """

        for _ in range(4):
            self = self.tilt().rotate()
        return type(self)(
            rows=self.rows, cols=self.cols, coords=tuple(sorted(self.coords))
        )

    def cycle(self, n):
        """
        Repeat the spin cycle `n` times:

            >>> print("-"); print(Grid.parse(sample).cycle(3).render())
            -
            .....#....
            ....#...O#
            .....##...
            ..O#......
            .....OOO#.
            .O#...O#.#
            ....O#...O
            .......OOO
            #...O###.O
            #.OOO#...O

        The sample repeats every 7 cycles:

            >>> for i in range(3, 11):
            ...     assert Grid.parse(sample).cycle(i) == Grid.parse(sample).cycle(i + 7)

        """
        cache = {}
        for i in range(n):
            self = self.spin()
            if (offset := cache.get(self)) is not None:
                period = i - offset
                break
            cache[self] = i
        else:
            return self

        return list(cache)[offset + (n - offset - 1) % period]


def solve1(input):
    """
    >>> solve1(sample)
    136
    """
    return Grid.parse(input).tilt().get_load()


def solve2(input):
    """
    >>> solve2(sample)
    64
    """
    return Grid.parse(input).cycle(1000000000).get_load()
