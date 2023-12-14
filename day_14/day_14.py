from typing import List
import time


def main():
    file = open("platform.txt", "r")
    lines = file.readlines()
    start = time.time()
    weight_shifted = calc_weight_shifted(lines)  # 110128
    print(f"weight : {weight_shifted} in {(time.time() - start) * 1000} ms")
    start = time.time()
    rotated = find_cycle(lines)  # 103861
    print(f"rotated: {rotated} in {(time.time() - start) * 1000} ms")
    file.close()


def find_cycle(lines: List[str]):
    platform = [line.strip() for line in lines]
    shifted_platform = platform[:]
    cache = []
    start, cycle_len = 0, 0
    for k in range(1_000_000_000):
        for i in range(4):
            shifted_platform = shift_platform_north(shifted_platform)
            shifted_platform = rotate_counter_clock(shifted_platform)
        calc_weight(shifted_platform)
        if shifted_platform in cache:
            start = cache.index(shifted_platform)  # cnt of shifts, not idx
            cycle_len = k - start  # shifts done - matched cnt
            target = (1_000_000_000 - start - 1) % cycle_len + start
            return calc_weight(cache[target])
        cache.append(shifted_platform)
    return start, cycle_len


def shift_platform_north(lines: List[str]):
    platform = lines[:]
    for col in range(len(platform[0].strip())):
        block_idx = 0
        for row in range(len(platform)):
            val = platform[row][col]
            if val == '#':
                block_idx = row + 1
            if val == 'O':
                platform[row] = platform[row][:col] + '.' + platform[row][col + 1:]
                platform[block_idx] = platform[block_idx][:col] + 'O' + platform[block_idx][col + 1:]
                block_idx += 1
    return platform


def calc_weight(lines: List[str]):
    sum_weights = 0
    for row, line in enumerate(lines):
        for char in line:
            if char == 'O':
                sum_weights += len(lines) - row
    return sum_weights


def calc_weight_shifted(lines: List[str]):
    sum_weights = 0
    for col in range(len(lines[0].strip())):
        # row of block and length of following items (rocks or cubes)
        block_idx = 0
        for row in range(len(lines)):
            val = lines[row][col]
            if val == '#':
                block_idx = row + 1
            # found cube or rock
            if val == 'O':
                # found rock
                sum_weights += len(lines) - block_idx
                block_idx += 1
    return sum_weights


def rotate_counter_clock(platform: List[str]):
    cols_as_rows = ["" for r in range(len(platform[0]))]
    for idx, line in enumerate(platform[::-1]):
        for i_col, col in enumerate(line):
            cols_as_rows[i_col] += col
    return cols_as_rows


if __name__ == "__main__":
    main()
