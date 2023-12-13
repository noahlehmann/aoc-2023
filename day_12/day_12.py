# this one broke things in my brain....

def main():
    file = open("springs.txt", "r")
    lines = file.readlines()
    cnt, expanded_cnt = 0, 0
    for line in lines:
        record, numbers = line.strip().split()
        numbers = tuple(int(x) for x in numbers.split(','))
        expanded_record = '?'.join([record] * 5)
        expanded_numbers = numbers * 5
        cnt += num_arrangements(record, numbers)
        expanded_cnt += num_arrangements(expanded_record, expanded_numbers)
    print(f"cnt normal  : {cnt}")  # 7670
    print(f"cnt expanded: {expanded_cnt}")  # 157383940585037
    file.close()


def num_arrangements(record, numbers):
    memoization_dict = {}

    # dynamic programming with memoization
    def num_arr(i_chars, k_nums):
        # subroutine to find num of arrangements, where we restrict to first i characters and first k nums
        if (i_chars, k_nums) in memoization_dict:
            # save time, reuse output
            return memoization_dict[(i_chars, k_nums)]
        if i_chars == 0 and k_nums == 0:
            return 1
        elif i_chars == 0:
            # no chars to process
            return 0
        elif k_nums == 0:
            # 1 if none of pattern is number, else 0
            return int(all(char != '#' for char in record[:i_chars]))
        elif record[i_chars - 1] == '.':
            # cannot be number, delegate rest of record for all numbers
            result = num_arr(i_chars - 1, k_nums)
        else:
            # last number
            num = numbers[k_nums - 1]
            # if number is bigger than len of record left or
            # if space of number from back of record contains '.'
            if num > i_chars or any(char == '.' for char in record[i_chars - num:i_chars]):
                result = 0
            # if more space than needed for number and
            # space at end of record for number starts with '#' -> number
            elif i_chars > num and record[i_chars - num - 1] == '#':
                result = 0
            else:
                result = num_arr(max(i_chars - num - 1, 0), k_nums - 1)
            # if char at last viewed spot is '?'
            # delegate to new function
            if record[i_chars - 1] == '?':
                result += num_arr(i_chars - 1, k_nums)
        # save computation
        memoization_dict[(i_chars, k_nums)] = result
        return result

    return num_arr(len(record), len(numbers))


if __name__ == "__main__":
    main()
