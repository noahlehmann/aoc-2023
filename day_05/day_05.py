from typing import List, Tuple


def main():
    file = open("almanac.txt", "r")
    lines = file.readlines()
    seeds, steps = split_steps(lines)
    print(calc_closest_location(tuple_seeds(seeds), steps)[0])
    print(calc_closest_location(calc_all_seeds(seeds), steps)[0])
    file.close()


def calc_closest_location(seeds: List[Tuple[int, int]], steps):
    source = seeds
    for step in steps:
        destination = map_source_to_destination(source, step)
        source = destination
    return min(source)


def tuple_seeds(seeds):
    return [(seed, 1) for seed in seeds]


def calc_all_seeds(seeds):
    all_seeds = []
    for i in range(0, len(seeds), 2):
        start = seeds[i]
        length = seeds[i+1]
        all_seeds.append((start, length))
    return all_seeds


def map_source_to_destination(source: List[Tuple[int, int]], step):
    destination = []
    unmapped = []
    for seed in source:
        match = False
        # if in range, break
        for r in step["ranges"]:
            range_start, range_end, movement = r["source"], r["source"] + r["range"] - 1, r["destination"] - r["source"]
            seed_start, seed_end = seed[0], seed[0] + seed[1] - 1
            seed_length = seed[1]
            if seed_end < range_start or range_end < seed_start:
                # no match
                continue
            elif range_start <= seed_start:
                # first parts matches
                if seed_end <= range_end:
                    # full match
                    destination.append((seed_start + movement, seed_length))
                    match = True
                else:
                    # take first part, recheck second
                    destination.append((seed_start + movement, range_end - seed_start + 1))
                    unmapped.append((range_end + 1, seed_end - range_end))
                    match = True
            elif seed_end <= range_end:
                unmapped.append((seed_start, range_start - seed_start))
                destination.append((range_start + movement, seed_end - range_start))
                match = True
        if not match:
            destination.append(seed)
    append = map_source_to_destination(unmapped, step) if len(unmapped) > 0 else []
    return destination + append


def split_steps(lines: List[str]):
    # get seeds as int array
    seeds = [int(seed) for seed in lines[0].split(":")[1].strip().split()]
    steps = []
    current_step = {}
    # skip seed line
    for line in lines[1:]:
        # is line only whitespaces and step is not empty
        if len(line.strip()) == 0:
            # save and reset step
            if current_step != {}:
                steps.append(current_step)
                current_step = {}
            # skip blank
            continue
        parts = line.split()
        # number or name of step
        if not parts[0].isdigit():
            current_step = {"name": parts[0], "ranges": []}
            continue
        # read values
        current_step["ranges"].append({
            "destination": int(parts[0]),
            "source": int(parts[1]),
            "range": int(parts[2])
        })
    # clear last step
    if current_step != {}:
        steps.append(current_step)
    return seeds, steps


if __name__ == "__main__":
    main()
