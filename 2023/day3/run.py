import re
from functools import reduce
from collections import defaultdict
from pathlib import Path


def read_lines_from_file(file_path):
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            yield line


def find_valid_part_number_and_symbol(schema, line_index, match):
    start_index = match.start()
    end_index = match.end()
    for check_line in [line_index - 1, line_index, line_index + 1]:
        if check_line < 0 or check_line >= len(schema):
            continue
        if check_line == line_index:
            check_indices = [start_index - 1, end_index]
        else:
            check_indices = range(start_index - 1, end_index + 1)

        for check_index in check_indices:
            if check_index < 0 or check_index >= len(schema[check_line]):
                continue
            if schema[check_line][check_index].isdigit():
                continue
            if schema[check_line][check_index] != ".":
                # print(f"Found {schema[check_line][check_index]} at line {check_line} and index {check_index}")
                yield True, (check_line, check_index)
    yield False, None


def sum_part_numbers(file_path):
    sum_ = 0
    schema = list(read_lines_from_file(file_path))
    for line_index, line in enumerate(schema):
        for match in re.finditer("\d+", line):
            # print(f"Number starts at index {start_index} and ends at index {end_index}")
            is_valid, _ = next(find_valid_part_number_and_symbol(schema, line_index, match))
            if is_valid:
                sum_ += int(match.group())
    print(sum_)


def sum_gear_ratios(file_path):
    schema = list(read_lines_from_file(file_path))

    potential_gears = defaultdict(list)

    for line_index, line in enumerate(schema):
        for match in re.finditer("\d+", line):
            is_valid, gear_coordinates = next(find_valid_part_number_and_symbol(schema, line_index, match))
            if is_valid:
                match_number = int(match.group())
                potential_gears[gear_coordinates].append(match_number)
    sum_ = 0
    for gear, gear_numbers in potential_gears.items():
        if len(gear_numbers) == 2:
            sum_ += reduce(lambda x, y: x * y, gear_numbers)
    print(sum_)


if __name__ == "__main__":
    file_path = Path(__file__).parent.joinpath("input.txt")

    sum_part_numbers(file_path)

    sum_gear_ratios(file_path)
