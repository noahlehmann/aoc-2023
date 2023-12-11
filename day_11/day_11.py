from typing import List, Tuple


def main():
    file = open("galaxy.txt", "r")
    lines = file.readlines()
    galaxies, free_rows, free_cols = scan_galaxies(lines)
    sum_dist = calc_distances(galaxies, free_rows, free_cols, 1)
    print(f"growth = 1   : {sum_dist}")  # 10289334
    sum_dist = calc_distances(galaxies, free_rows, free_cols, 1_000_000)
    print(f"growth = 1mio: {sum_dist}")  # 10289334
    file.close()


def calc_distances(galaxies: List[Tuple[int, int]], free_rows, free_cols, growth):
    growth = growth - 1 if growth > 1 else 1
    sum_dist = 0
    for i_galaxy in range(0, len(galaxies)):
        galaxy = galaxies[i_galaxy]
        for i_other in range(i_galaxy, len(galaxies)):
            other = galaxies[i_other]
            row_adjust, col_adjust = 0, 0
            # adjust
            for idx in free_rows:
                if idx in build_range(galaxy[0], other[0] + 1):
                    row_adjust += growth
            for idx in free_cols:
                if idx in build_range(galaxy[1], other[1] + 1):
                    col_adjust += growth
            # calc
            distance = abs(other[0] - galaxy[0]) + abs(other[1] - galaxy[1])
            distance += row_adjust + col_adjust
            sum_dist += distance
    return sum_dist


def build_range(a, b):
    return range(a, b) if a <= b else range(b, a)


def scan_galaxies(lines: List[str]):
    galaxies = []
    non_free_cols, non_free_rows = [], []
    for row in range(0, len(lines)):
        for col in range(0, len(lines[row].strip())):
            if lines[row][col] == "#":
                galaxies.append((row, col))
                non_free_cols.append(col)
                non_free_rows.append(row)
    free_rows = list(filter(lambda x: x not in non_free_rows, range(len(lines))))
    free_cols = list(filter(lambda x: x not in non_free_cols, range(len(lines[0].strip()))))
    return galaxies, free_rows, free_cols


if __name__ == "__main__":
    main()
