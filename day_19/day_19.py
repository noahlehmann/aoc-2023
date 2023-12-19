from typing import Dict, List, Tuple


def main():
    file = open("sort.txt", "r")
    lines = file.read().split("\n")
    parts, flows = parse(lines)
    accepted_parts = []
    for part in parts:
        if is_accepted(flows, "in", part):
            accepted_parts.append(part)
    print(f"accepted     : {sum_up(accepted_parts)}")  # 432427
    min_max = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
    limits = iterate_tree_min_max(flows, "in", min_max)
    sum_pos = 0
    for limit in limits:
        possibilities = 1
        for k in limit:
            if limit[k][0] >= limit[k][1]:
                continue  # no values between
            possibilities *= limit[k][1] - limit[k][0] + 1
        sum_pos += possibilities
    print(f"possibilities: {sum_pos}")
    file.close()


def iterate_tree_min_max(flows, first, min_max: Dict[str, Tuple[int, int]]) -> List[Dict[str, Tuple[int, int]]]:
    prev, outcomes, all_limits = [], [], []
    for rule in flows[first]["steps"].keys():
        copy, xmas, sign, val = min_max.copy(), rule[0], rule[1], int(rule[2:])  # init
        apply_prev_reverse(prev, copy)  # apply reversed rules from prev steps
        set_new_limits(copy, xmas, sign, val)  # set current step
        prev.append((xmas, sign, val))
        outcome = flows[first]["steps"][rule]
        handle_outcome(outcome, flows, copy, all_limits)
    # handle default
    copy = min_max.copy()
    apply_prev_reverse(prev, copy)
    handle_outcome(flows[first]["default"], flows, copy, all_limits)
    return all_limits


def handle_outcome(outcome, flows, min_max, all_limits):
    if outcome == "R":
        # skip rejected
        pass
    elif outcome == "A":
        all_limits.append(min_max)
    else:
        # delegate
        all_limits += iterate_tree_min_max(flows, outcome, min_max)


def set_new_limits(min_max, xmas, sign, val):
    if sign == ">":  # min
        new_min = val + 1 if val + 1 > min_max[xmas][0] else min_max[xmas][0]
        min_max[xmas] = (new_min, min_max[xmas][1])
    else:  # max
        new_max = val - 1 if val - 1 < min_max[xmas][1] else min_max[xmas][1]
        min_max[xmas] = (min_max[xmas][0], new_max)


def apply_prev_reverse(prev: List[Tuple[int, int, int]], min_max):
    for p in prev:
        xmas, sign, val = p[0], p[1], p[2]
        if sign == ">":  # min
            # set max <= val
            min_max[xmas] = (min_max[xmas][0], val)
        else:  # "<" max
            # set min <= val
            min_max[xmas] = (val, min_max[xmas][1])


def sum_up(parts):
    sum_parts = 0
    for part in parts:
        for k in part.keys():
            sum_parts += part[k]
    return sum_parts


def is_accepted(flows, first, part):
    default = flows[first]["default"]
    x, m, a, s = part["x"], part["m"], part["a"], part["s"]
    for step in flows[first]["steps"].keys():
        if eval(step):
            default = flows[first]["steps"][step]
            break
        else:
            continue
    if default in ["A", "R"]:
        return True if default == "A" else False
    else:
        return is_accepted(flows, default, part)


def parse(lines):
    flows = {}
    parts = []
    for line in lines:
        if len(line.strip()) == 0:
            continue
        if line[0] == "{":
            split = line[1:len(line) - 1].split(",")
            part = {}
            for p in split:
                prop, val = p.split("=")
                part[prop] = int(val)
            parts.append(part)
        else:
            name, rule = line[:len(line) - 1].split("{")
            rs = rule.split(",")
            default = rs[len(rs) - 1]
            steps = {}
            for r in rs[:len(rs) - 1]:
                expr, to = r.split(":")
                steps[expr] = to
            flows[name] = {
                "steps": steps,
                "default": default
            }
    return parts, flows


if __name__ == "__main__":
    main()
