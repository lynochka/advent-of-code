from pathlib import Path
from functools import reduce

CONTENTS = {"red": 12, "green": 13, "blue": 14}


def read_lines_from_file(file_path):
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            yield line


def sum_valid_game_ids(file_path):
    valid_game_ids_sum = 0
    for line in read_lines_from_file(file_path):
        valid_game_ids_sum += validate_game(line)

    return valid_game_ids_sum


def sum_game_powers(file_path):
    game_power_sum = 0
    for line in read_lines_from_file(file_path):
        _, subline_game = split_game_line(line)
        game_power_sum += find_game_power(subline_game)

    return game_power_sum


def split_game_line(line):
    """Return game ID and subline for subgames."""
    line = line.strip()
    subline_game_id, subline_game = line.split(":")[:2]
    return subline_game_id.split(" ")[1].strip(), subline_game.strip()


def validate_game(line):
    game_id, subline_game = split_game_line(line)
    subgames = subline_game.split(";")

    for subgame in subgames:
        subgame = subgame.strip()
        if not validate_subgame(subgame):
            return 0
    return int(game_id)


def validate_subgame(line):
    for cube_color_count in line.split(","):
        cube_count, cube_color = cube_color_count.strip().split(" ")
        contents_color_cube_count = CONTENTS.get(cube_color.strip(), 0)
        if contents_color_cube_count < int(cube_count.strip()):
            return False
    return True


def find_game_power(subline_game):
    min_color_count = dict()

    for line in subline_game.split(";"):
        line = line.strip()

        for cube_color_count in line.split(","):
            cube_count_str, cube_color = cube_color_count.strip().split(" ")
            cube_color = cube_color.strip()
            cube_count = int(cube_count_str.strip())
            if min_color_count.get(cube_color, 0) < cube_count:
                min_color_count[cube_color] = cube_count
    return reduce(lambda x, y: x * y, min_color_count.values())


if __name__ == "__main__":
    file_path = Path(__file__).parent.joinpath("example.txt")

    result = sum_valid_game_ids(file_path)
    print(result)

    result = sum_game_powers(file_path)
    print(result)
