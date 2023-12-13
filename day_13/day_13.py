from typing import List


def main():
    file = open("mirrors.txt", "r")
    lines = file.readlines()
    fields = parse_fields(lines)
    cnt, cnt_smudge = find_all_reflections(fields)
    print(f"cnt   : {cnt}")  # 29165
    print(f"smudge: {cnt_smudge}")  # 32192
    file.close()


def find_all_reflections(fields):
    cnt = 0
    smudge = 0
    for field in fields:
        above, left = find_reflections(field, 0)
        above_smudge, left_smudge = find_reflections(field, 1, (above, left))
        cnt += above * 100 if above is not None else left
        # what is new reflection?
        smudge += above_smudge * 100 if above_smudge is not None and above_smudge != above else left_smudge if left_smudge is not None else above * 100
    return cnt, smudge


def find_reflections(field: List[str], threshold: int, skip=None):
    cols_as_rows = mirror_rows(field)
    if skip is not None:
        above = find_above_reflection(field, threshold, skip[0])
        left = find_above_reflection(cols_as_rows, threshold, skip[1])
    else:
        above = find_above_reflection(field, threshold)
        left = find_above_reflection(cols_as_rows, threshold)
    return above, left


def mirror_rows(field: List[str]):
    cols_as_rows = ["" for r in range(0, len(field[0]))]
    for idx, line in enumerate(field):
        for i_col, col in enumerate(line):
            cols_as_rows[i_col] += col
    return cols_as_rows


def find_above_reflection(field: List[str], threshold, skip=None):
    for idx, line in enumerate(field):
        if idx == skip:
            continue
        after, before = idx, idx - 1
        num_diffs = sum(a != b for a, b in zip(field[after], field[before]))
        try:
            # same or 'almost same' is mirror
            # iterate until out of bounds -> all mirror
            while num_diffs <= threshold:
                after += 1
                before -= 1
                num_diffs = sum(a != b for a, b in zip(field[after], field[before]))
                if before < 0 and idx != 0:
                    return idx
        except IndexError:
            return idx
    return None


def parse_fields(lines: List[str]):
    fields = []
    current = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            fields.append(current)
            current = []
        else:
            current.append(line)
    if len(current) > 0:
        fields.append(current)
    return fields


if __name__ == "__main__":
    main()
