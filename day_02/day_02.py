from enum import Enum
from typing import List


class Config(Enum):
    RED = 12
    GREEN = 13
    BLUE = 14


def main():
    games = open("games.txt", "r")
    lines = games.readlines()
    find_possible(lines)
    find_powers(lines)
    games.close()


def find_possible(lines: List[str]):
    id_sum = 0
    for line in lines:
        id_start = line.find(" ") + 1
        id_end = line.find(":")
        game_id = line[id_start:id_end]
        picks = line[id_end+1:].split(";")
        color_dict = extract_color_dict(picks)
        fits = True
        if max(color_dict['red']) > Config.RED.value:
            fits = False
        if max(color_dict['green']) > Config.GREEN.value:
            fits = False
        if max(color_dict['blue']) > Config.BLUE.value:
            fits = False
        if fits:
            id_sum += int(game_id)
    print(id_sum)


def find_powers(lines: List[str]):
    power_sum = 0
    for line in lines:
        parts = line.split(":")
        picks = parts[1].split(";")
        color_dict = extract_color_dict(picks)
        red = max(color_dict["red"])
        green = max(color_dict["green"])
        blue = max(color_dict["blue"])
        power_sum += (red * green * blue)
    print(power_sum)


def extract_color_dict(picks: List[str]):
    color_dict = {
        "red": [],
        "green": [],
        "blue": []
    }
    for pick in picks:
        values = pick.split(",")
        for value in values:
            parts = value.strip().split(" ")
            number = parts[0].strip()
            color = parts[1].strip()
            color_dict[color.lower()].append(int(number))
    return color_dict


if __name__ == "__main__":
    main()