from typing import List, Dict
from collections import defaultdict
import sys
import math


def main():
    file = open("maps.txt", "r")
    lines = file.readlines()
    lr_sequence, steps = parse_map(lines)
    step_cnt = walk_steps_rec(steps, "AAA", lr_sequence, 0, lambda step: step == "ZZZ")
    print(f"regular: {step_cnt}")  # 19667
    # naive solution
    # step_cnt = walk_steps_iter(steps, lr_sequence)
    step_cnt = calc_ghost_steps(steps, lr_sequence)
    print(f"ghost  : {step_cnt}")  # 19185263738117
    file.close()


def parse_map(lines: List[str]):
    lr_sequence = lines[0].strip()
    steps = {}
    for i in range(2, len(lines)):
        line = lines[i]
        parts = line.split("=")
        step = parts[0].strip()
        pair = parts[1].strip()[1:9].split(",")
        steps[step] = (pair[0].strip(), pair[1].strip())
    return lr_sequence, steps


def walk_steps_rec(steps: Dict, current_step, seq, seq_idx, stop_func) -> int:
    if stop_func(current_step):
        return 0
    l_r = 0 if seq[seq_idx] == "L" else 1
    next_step = steps[current_step][l_r]
    next_seq_idx = 0 if len(seq) - 1 == seq_idx else seq_idx + 1
    return walk_steps_rec(steps, next_step, seq, next_seq_idx, stop_func) + 1


def walk_steps_iter(steps: Dict, seq):
    step_cnt = 0
    seq_idx = 0
    current_steps = [step for step in steps.keys() if step[2] == "A"]
    while not all_end_on_z(current_steps) and step_cnt < 20:
        print(current_steps)
        l_r = 0 if seq[seq_idx] == "L" else 1
        seq_idx = 0 if len(seq) - 1 == seq_idx else seq_idx + 1
        current_steps = [steps[step][l_r] for step in current_steps]
        step_cnt += 1
    print(current_steps)
    return step_cnt


def all_end_on_z(steps: List) -> bool:
    return all([step[2] == "Z" for step in steps])


def calc_ghost_steps(steps: Dict, seq):
    starts = [k for k in steps.keys() if k[2] == "A"]
    steps_taken = [walk_steps_rec(steps, start, seq, 0, lambda step: step[2] == "Z") for start in starts]
    return lcm(steps_taken)


def lcm(numbers: List):
    max_factor_multiplicities = defaultdict(int)
    for num in numbers:
        for prime, multiplicity in prime_factors(num).items():
            max_factor_multiplicities[prime] = max(max_factor_multiplicities[prime], multiplicity)
    result = 1
    for prime, multiplicity in max_factor_multiplicities.items():
        result *= prime ** multiplicity
    return result


def prime_factors(n):
    factors = defaultdict(int)
    while n % 2 == 0:
        factors[2] += 1
        n //= 2
    for i in range(3, math.isqrt(n) + 1, 2):
        while n % i == 0:
            factors[i] += 1
            n //= i
    if n > 2:
        factors[n] += 1
    return factors


if __name__ == "__main__":
    recursion_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(30_000)
    main()
    sys.setrecursionlimit(recursion_limit)
