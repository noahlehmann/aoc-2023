# not proud of this, first it was very early, then very late... busy sunday

from typing import List
import re


#   0
# 3 p 1
#   2
pipes = {
    "|": {"i": 0, "o": 2},
    "-": {"i": 3, "o": 1},
    "L": {"i": 0, "o": 1},
    "J": {"i": 0, "o": 3},
    "7": {"i": 3, "o": 2},
    "F": {"i": 1, "o": 2},
}


class DoesNotConnect(Exception):
    pass


def main():
    file = open("pipes.txt", "r")
    lines = file.readlines()
    path, furthest = find_furthest_path(lines)
    enclosure = calc_enclosure(lines, path)
    print(f"furthest : {furthest}")  # 7063, path.len = 14126
    print(f"enclosure: {enclosure}")  # 589
    file.close()


def replace_with_visual(path):
    replace = {
        "|": "║",
        "-": "═",
        "F": "╔",
        "L": "╚",
        "7": "╗",
        "J": "╝",
    }
    return replace.get(path)


def intersects(path: str):
    pattern = r'F.*J|\||L.*7'
    return re.match(pattern, path) is not None


def calc_enclosure(lines: List, path: List):
    cnt = 0
    # skip first and last row
    for row in range(0, len(lines)):
        out = True
        following = ""
        # visual = ""
        for col in range(0, len(lines[row])):
            in_path = any([val["row"] == row and val["col"] == col for val in path])
            if in_path:
                char = lines[row][col]
                following += char if char != "S" else "J"
                # visual += replace_with_visual(char) if char != "S" else "S"
                if intersects(following):
                    following = ""
                    out = not out
                elif len(following) >= 2 and following[len(following) - 1] != "-":
                    following = ""
            else:
                following = ""
                if not out:
                    cnt += 1
                    # visual += "°"
                #else:
                #    visual += " "
        # print(f"{visual}   - l. {row}")
    return cnt


def find_furthest_path(lines: List[str]):
    grid, tunnel = convert_grid(lines)
    path = follow_path(grid, tunnel)
    return path, int((len(path)) / 2)


def convert_grid(lines):
    grid = []
    start = {}
    tunnel = []
    for row in range(0, len(lines)):
        grid.append([])
        line = lines[row].strip()
        for col in range(0, len(line)):
            pipe = line[col]
            grid[row].append(pipe)
            if pipe == "S":
                start["row"] = row
                start["col"] = col
                start["pipe"] = "S"
                tunnel.append(start)
    return grid, tunnel


def follow_path(grid: List[List[str]], tunnel: List):
    start = tunnel[0]
    possibles = get_possibles(start, grid)
    last, next_naive = start, possibles.pop()
    next_naive["pipe"] = grid[next_naive["row"]][next_naive["col"]]
    tunnel.append(next_naive)
    while next_naive["pipe"] != "S" and len(possibles) > 0:
        try:
            if next_naive["pipe"] == ".":
                raise DoesNotConnect
            current = next_naive
            current["pipe"] = grid[current["row"]][current["col"]]
            pos = map_i_o(last, current)
            next_naive = {"row": pos["row"], "col": pos["col"], "pipe": grid[pos["row"]][pos["col"]]}
            tunnel.append(next_naive)
            last = current
        except DoesNotConnect:
            last = start
            next_naive = possibles.pop()
            next_naive["pipe"] = grid[next_naive["row"]][next_naive["col"]]
            tunnel = [start, next_naive]
    return tunnel


def get_possibles(start, grid):
    to_remove, final = [], []
    possibles = {
        "top": {"row": start["row"] - 1, "col": start["col"]},  # top
        "right": {"row": start["row"], "col": start["col"] + 1},  # right
        "bottom": {"row": start["row"] + 1, "col": start["col"]},  # bottom
        "left": {"row": start["row"], "col": start["col"] - 1},  # left
    }
    if get_char(grid, possibles["top"]) in ["-", "J", "L"]:  # top
        to_remove.append("top")
    if get_char(grid, possibles["right"]) in ["|", "L", "F"]:  # right
        to_remove.append("right")
    if get_char(grid, possibles["bottom"]) in ["F", "-", "7"]:  # bottom
        to_remove.append("bottom")
    if get_char(grid, possibles["left"]) in ["|", "7", "J"]:  # left
        to_remove.append("left")
    for key in possibles.keys():
        if key not in to_remove:
            final.append(possibles.get(key))
    final = list(filter(lambda val: val["row"] >= 0 and val["col"] >= 0, final))
    return final


def get_char(grid, pos):
    return grid[pos["row"]][pos["col"]]


def map_i_o(last, current):
    if current["pipe"] == "|":
        if last["row"] < current["row"]:
            # from top
            if last["pipe"] in ["-", "J", "L"]:
                raise DoesNotConnect
            return {"row": current["row"] + 1, "col": current["col"]}
        else:
            # from bottom
            if last["pipe"] in ["-", "F", "7"]:
                raise DoesNotConnect
            return {"row": current["row"] - 1, "col": current["col"]}
    if current["pipe"] == "-":
        # from left
        if last["col"] < current["col"]:
            if last["pipe"] in ["|", "7", "J"]:
                raise DoesNotConnect
            return {"row": current["row"], "col": current["col"] + 1}
        else:
            # from right
            if last["pipe"] in ["|", "L", "F"]:
                raise DoesNotConnect
            return {"row": current["row"], "col": current["col"] - 1}
    if current["pipe"] == "L":
        # from top
        if last["row"] < current["row"]:
            if last["pipe"] in ["-", "J", "L"]:
                raise DoesNotConnect
            return {"row": current["row"], "col": current["col"] + 1}
        else:
            # from right
            if last["pipe"] in ["|", "F", "L"]:
                raise DoesNotConnect
            return {"row": current["row"] - 1, "col": current["col"]}
    if current["pipe"] == "J":
        # from top
        if last["row"] < current["row"]:
            if last["pipe"] in ["-", "L", "J"]:
                raise DoesNotConnect
            return {"row": current["row"], "col": current["col"] - 1}
        else:
            # from left
            if last["pipe"] in ["|", "J", "7"]:
                raise DoesNotConnect
            return {"row": current["row"] - 1, "col": current["col"]}
    if current["pipe"] == "7":
        # from left
        if last["row"] == current["row"]:
            if last["pipe"] in ["|", "7", "J"]:
                raise DoesNotConnect
            return {"row": current["row"] + 1, "col": current["col"]}
        else:
            # from bottom
            if last["pipe"] in ["7", "F", "-"]:
                raise DoesNotConnect
            return {"row": current["row"], "col": current["col"] - 1}
    if current["pipe"] == "F":
        # from right
        if last["row"] == current["row"]:
            if last["pipe"] in ["|", "F", "L"]:
                raise DoesNotConnect
            return {"row": current["row"] + 1, "col": current["col"]}
        else:
            # from bottom
            if last["pipe"] in ["F", "-", "7"]:
                raise DoesNotConnect
            return {"row": current["row"], "col": current["col"] + 1}
    return -1


if __name__ == "__main__":
    main()
