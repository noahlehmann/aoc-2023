import sys
from typing import Tuple, List, Set

directions = {
    "-": {
        "TOP": [((0, -1), "RIGHT"), ((0, 1), "LEFT")],
        "RIGHT": [((0, -1), "RIGHT")],
        "BOTTOM": [((0, -1), "RIGHT"), ((0, 1), "LEFT")],
        "LEFT": [((0, 1), "LEFT")],
    },
    "|": {
        "TOP": [((1, 0), "TOP")],
        "RIGHT": [((-1, 0), "BOTTOM"), ((1, 0), "TOP")],
        "BOTTOM": [((-1, 0), "BOTTOM")],
        "LEFT": [((-1, 0), "BOTTOM"), ((1, 0), "TOP")],
    },
    "/": {
        "TOP": [((0, -1), "RIGHT")],
        "RIGHT": [((1, 0), "TOP")],
        "BOTTOM": [((0, 1), "LEFT")],
        "LEFT": [((-1, 0), "BOTTOM")],
    },
    "\\": {
        "TOP": [((0, 1), "LEFT")],
        "RIGHT": [((-1, 0), "BOTTOM")],
        "BOTTOM": [((0, -1), "RIGHT")],
        "LEFT": [((1, 0), "TOP")],
    },
    ".": {
        "TOP": [((1, 0), "TOP")],
        "RIGHT": [((0, -1), "RIGHT")],
        "BOTTOM": [((-1, 0), "BOTTOM")],
        "LEFT": [((0, 1), "LEFT")],
    }
}


def main():
    file = open("light.txt", "r")
    lines = file.read().split("\n")
    lit_points = follow_beam_from((0, 0), "LEFT", lines, set())
    only_p = set(p for p, s in lit_points)
    print(f"points: {len(only_p)}")  # 6605
    ups = find_largest_from_points_and_source([(0, col) for col in range(len(lines[0]))], "TOP", lines)
    rights = find_largest_from_points_and_source([(row, len(lines[0]) - 1) for row in range(len(lines))], "RIGHT", lines)
    bottoms = find_largest_from_points_and_source([(len(lines) - 1, col) for col in range(len(lines[0]))], "BOTTOM", lines)
    lefts = find_largest_from_points_and_source([(row, 0) for row in range(len(lines))], "LEFT", lines)
    print(f"max ps: {max(ups, rights, bottoms, lefts)}")  # 6766
    file.close()


def find_largest_from_points_and_source(points, source, lines):
    all_lit = []
    for point in points:
        lit = follow_beam_from(point, source, lines, set())
        x = len(set(p for p, s in lit))
        all_lit.append(x)
    return max(all_lit)


def follow_beam_from(point: Tuple[int, int], source: str, lines: List[str],
                     path: Set[Tuple[Tuple[int, int], str]]):
    row_bounds = range(0, len(lines))
    col_bounds = range(0, len(lines[0]))
    if point[0] not in row_bounds or point[1] not in col_bounds:
        return path
    if (point, source) in path:
        return path
    path.add((point, source))
    next_points = directions[lines[point[0]][point[1]]][source]
    for p, s in next_points:
        n = (point[0] + p[0], point[1] + p[1])
        path |= follow_beam_from(n, s, lines, path)
    return path


if __name__ == "__main__":
    rec = sys.getrecursionlimit()
    sys.setrecursionlimit(rec * 10)
    main()
    sys.setrecursionlimit(rec)
