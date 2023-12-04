from typing import List


def main():
    file = open("cards.txt", "r")
    lines = file.readlines()
    count_wins(lines)
    count_cards(lines)
    file.close()


def count_cards(lines: List[str]):
    card_cnt = [1] * len(lines)
    for i in range(0, len(lines)):
        numbers = lines[i].split(":")[1].split("|")
        wins = [int(num) for num in numbers[0].strip().split()]
        actual = [int(num) for num in numbers[1].strip().split()]
        matches = [w for w in wins if w in actual]
        for k in range(i + 1, i + len(matches) + 1):
            card_cnt[k] += card_cnt[i]
    card_sum = 0
    for cnt in card_cnt:
        card_sum += cnt
    print(card_sum)


def count_wins(lines: List[str]):
    win_sum = 0
    for line in lines:
        numbers = line.split(":")[1].split("|")
        wins = [int(num) for num in numbers[0].strip().split()]
        actual = [int(num) for num in numbers[1].strip().split()]
        matches = [w for w in wins if w in actual]
        win_sum += calc_streak(len(matches))
    print(win_sum)


def calc_streak(length: int):
    if length <= 0:
        return 0
    if length == 1:
        return 1
    else:
        return calc_streak(length - 1) * 2


if __name__ == "__main__":
    main()