from typing import List


def main():
    file = open("engine.txt", "r")
    lines = file.readlines()
    engine_numbers(lines)
    find_gears(lines)
    file.close()


def find_gears(lines: List[str]):
    sum_prod_gears = 0
    numbers, symbols = extract_info(lines)
    gears = list(filter(lambda symbol: symbol["val"] == "*", symbols))
    print(len(gears))
    for gear in gears:
        matches = []
        for number in numbers:
            possible_rows = possible_rows_for_match(gear)
            possible_cols = possible_cols_for_match(gear)
            actual_cols = list(range(number["col"], number["col"] + len(number["val"])))
            if number["row"] in possible_rows and len([possible for possible in possible_cols if possible in actual_cols]) > 0:
                matches.append(int(number["val"]))
        if len(matches) == 2:
            sum_prod_gears += matches[0] * matches[1]
    print(sum_prod_gears)


def engine_numbers(lines: List[str]):
    sum_numbers = 0
    numbers, symbols = extract_info(lines)
    for number in numbers:
        possible_rows = possible_rows_for_match(number)
        possible_cols = possible_cols_for_match(number)
        if any(symbol["row"] in possible_rows and symbol["col"] in possible_cols for symbol in symbols):
            sum_numbers += int(number["val"])
    print(sum_numbers)


def possible_rows_for_match(number):
    row = number["row"]
    return [row-1, row, row+1]


def possible_cols_for_match(number):
    col = number["col"]
    return list(range(col-1, col + len(number["val"])+1))


def extract_info(lines: List[str]):
    chars = []
    numbers = []
    # iterate over all chars
    for row in range(0, len(lines)):
        line = lines[row]
        current_number = ""
        for col in range(0, len(line)):
            char = line[col]
            if char.isdigit():
                current_number += char
            elif char != "." and char != "\n":
                chars.append({"row": row, "col": col, "val": char})
                if len(current_number) > 0:
                    numbers.append({"row": row, "col": col - len(current_number), "val": current_number})
                    current_number = ""
            else:
                if len(current_number) > 0:
                    numbers.append({"row": row, "col": col - len(current_number), "val": current_number})
                    current_number = ""
        if len(current_number) > 0:
            numbers.append({"row": row, "col": len(lines[row]) - len(current_number), "val": current_number})
            current_number = ""
    return numbers, chars


if __name__ == "__main__":
    main()