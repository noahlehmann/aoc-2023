from typing import Dict


def main():
    file = open("init.txt", "r")
    line = file.read().strip()
    verification = verify_init_seq(line)
    print(f"verify: {verification}")  # 516070
    lenses = calc_focus_power(set_lenses(line))
    print(f"lenses: {lenses}")  # 244981
    file.close()


def calc_focus_power(boxes: Dict[int, Dict[str, int]]) -> int:
    sum_focus = 0
    for box_key in boxes:
        for lens_idx, lens_key in enumerate(boxes[box_key]):
            a, b, c = (box_key + 1), (lens_idx + 1), boxes[box_key][lens_key]
            sum_focus += a * b * c
    return sum_focus


def hash_string(string):
    current_value = 0
    for char in string:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


def set_lenses(seq):
    steps = seq.split(',')
    boxes = {}
    for step in steps:
        if step[len(step) - 1] == '-':
            label = step[:len(step) - 1]
            box = hash_string(label)
            handle_map(boxes, box, label, 0, remove=True)
        else:
            l, num = step.split("=")
            box = hash_string(l)
            handle_map(boxes, box, l, int(num), remove=False)
    return boxes


def handle_map(hash_map: Dict[int, Dict[str, int]], box: int, label: str, num: int, remove: bool):
    if box in hash_map.keys():
        if remove:
            hash_map[box].pop(label, None)
            if len(hash_map[box]) == 0:
                hash_map.pop(box)
        else:
            # replaces or sets key with num
            hash_map[box][label] = num
    elif not remove:
        # init box with dict containing one key
        hash_map[box] = {label: num}


def verify_init_seq(seq):
    sum_hash = 0
    for string in seq.split(","):
        sum_hash += hash_string(string)
    return sum_hash


if __name__ == "__main__":
    main()
