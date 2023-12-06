from typing import List


def main():
    file = open("races.txt", "r")
    lines = file.readlines()
    times = retrieve_values(lines[0])
    distances = retrieve_values(lines[1])
    print(f"times    : {times}")
    print(f"distances: {distances}")
    calc_margin_of_error(times, distances)
    time_arr = [int("".join([str(val) for val in times]))]
    dist_arr = [int("".join([str(val) for val in distances]))]
    calc_margin_of_error(time_arr, dist_arr)
    file.close()


def retrieve_values(line: str):
    return [int(val) for val in line.split(":")[1].strip().split()]


def calc_margin_of_error(times: List[int], distances: List[int]):
    product = 1
    sum_ways = 0
    for i in range(0, len(times)):
        time, dist = times[i], distances[i]
        wins = find_faster_ways(time, dist)
        product *= len(wins) if len(wins) > 0 else 1
        sum_ways += len(wins)
    print(f"margin: {product}")
    print(f"ways  : {sum_ways}")


def find_faster_ways(time: int, dist: int):
    ways = []
    # 0 and time don't move at all
    for sec in range(1, time):
        time_left = time - sec
        speed = sec
        travelled = speed * time_left
        if travelled > dist:
            ways.append(travelled)
    return ways


if __name__ == "__main__":
    main()
