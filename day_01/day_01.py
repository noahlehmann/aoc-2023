numbers = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
}


def main():
    find_digits()
    find_corrected()


def find_digits():
    file = open("calibration.txt", "r")
    lines = file.readlines()
    calibration_sum = 0
    for line in lines:
        first, i_first = find_first_digit(line)
        last, i_last_rev = find_first_digit(line[::-1])
        calibration_sum += int(f"{first}{last}")
    print(calibration_sum)


def find_corrected():
    file = open("calibration.txt", "r")
    lines = file.readlines()
    calibration_sum = 0
    for line in lines:
        first = find_spelled(line, True)
        last = find_spelled(line, False)
        calibration_sum += int(f"{first}{last}")
    print(calibration_sum)


def find_first_digit(calibration: str):
    for i in range(0, len(calibration)):
        if calibration[i].isdigit():
            return calibration[i], i


def find_spelled(calibration_str: str, first: bool):
    number, i_number, word, i_word = None, None, -1, -1
    words_idx = find_all_words(calibration_str, first)
    if first:
        number, i_number = find_first_digit(calibration_str)
    else:
        number, i_number = find_first_digit(calibration_str[::-1])
        i_number = len(calibration_str) - i_number

    if len(words_idx) == 0:
        return number
    elif first:
        i_word = min(words_idx)
    else:
        i_word = max(words_idx)
    word = words_idx.get(i_word)
    if first:
        return number if i_number < i_word else word
    else:
        return number if i_number > i_word else word


def find_all_words(calibration: str, first) -> dict:
    words = {}
    for key in numbers.keys():
        if first:
            idx = calibration.find(numbers.get(key))
        else:
            idx = calibration.rfind(numbers.get(key))
        if not idx == -1:
            words[idx] = key
    return words


if __name__ == "__main__":
    main()
