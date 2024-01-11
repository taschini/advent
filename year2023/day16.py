# https://adventofcode.com/2023/day/16

sample = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""


def solve1(input):
    """
    >>> solve1(sample)
    46
    """
    return count_energized(input.splitlines(), 0, -1)


def count_energized(raster, i, j):
    rows = len(raster)
    cols = len(raster[0])
    energized = set()
    visited = set()

    dj = max(0, -j) + min(cols - j - 1, 0)
    di = max(0, -i) + min(rows - i - 1, 0)
    assert abs(di) + abs(dj) == 1
    beams = [(i, j, di, dj)]

    while beams:
        i, j, di, dj = beams.pop()
        i += di
        j += dj

        if 0 <= i < rows and 0 <= j < cols and (i, j, di, dj) not in visited:
            energized.add((i, j))
            visited.add((i, j, di, dj))
            match raster[i][j]:
                case "\\":
                    beams.append((i, j, dj, di))
                case "/":
                    beams.append((i, j, -dj, -di))
                case "-" if dj == 0:
                    beams.append((i, j, 0, +1))
                    beams.append((i, j, 0, -1))
                case "|" if di == 0:
                    beams.append((i, j, +1, 0))
                    beams.append((i, j, -1, 0))
                case _:
                    beams.append((i, j, di, dj))
    return len(energized)


def solve2(input):
    """
    >>> solve2(sample)
    51
    """
    raster = input.splitlines()
    rows = len(raster)
    cols = len(raster[0])
    starts = (
        [(i, -1) for i in range(rows)]
        + [(-1, j) for j in range(cols)]
        + [(i, cols) for i in range(rows)]
        + [(rows, j) for j in range(cols)]
    )
    return max(count_energized(raster, *start) for start in starts)
