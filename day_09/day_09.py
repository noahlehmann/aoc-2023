from typing import List


def main():
    file = open("report.txt", "r")
    lines = file.readlines()
    sums_next, sums_prev = 0, 0
    for report in parse_report(lines):
        prev_val, next_val = find_next_val_rec(report)
        sums_prev += prev_val
        sums_next += next_val
    print(f"next: {sums_next}")
    print(f"prev: {sums_prev}")
    file.close()


def find_next_val_rec(seq: List[int]):
    if all_zeros(seq):
        # stop_recursion
        return 0
    vals = find_next_val_rec(get_diffs(seq))
    # all values same
    if vals == 0:
        return seq[0], seq[0]
    else:
        next_val = seq[len(seq) - 1] + vals[1]
        prev_val = seq[0] - vals[0]
        return prev_val, next_val


def parse_report(lines: List):
    return [[int(val) for val in line.strip().split()] for line in lines]


def get_diffs(vals: List[int]):
    diffs = []
    for i in range(1, len(vals)):
        diffs.append(vals[i] - vals[i-1])
    return diffs


def all_zeros(vals: List[int]):
    return all([val == 0 for val in vals])


if __name__ == "__main__":
    main()
