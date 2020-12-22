import re
from copy import copy
from math import prod


def transpose(tile):
    return list(map(lambda x: "".join(x), zip(*tile)))


def get_side(tile, direction):
    assert direction in ("N", "S", "W", "E")
    if direction == "N":
        return tile[0]
    if direction == "S":
        return tile[-1]

    tile_transpose = transpose(tile)
    if direction == "W":
        return tile_transpose[0]
    if direction == "E":
        return tile_transpose[-1]
    raise RuntimeError("'direction' should be 'N', 'S', 'W', or 'E'!")


tile = [".$#", ".##", "#@@"]
assert "..#" == get_side(tile, "W")
assert "##@" == get_side(tile, "E")
assert tile[0] == get_side(tile, "N")
assert tile[-1] == get_side(tile, "S")


def rotate_90(tile):
    return list(map(lambda x: "".join(x), zip(*reversed(tile))))


def rotate_n_90(tile, n):
    """
    n is the number of times we rotate
    """
    new_tile = copy(tile)
    for i in range(n):
        new_tile = rotate_90(new_tile)
    return new_tile


tile = ["12", "34"]
assert ["31", "42"] == rotate_n_90(tile, 1)
assert ["43", "21"] == rotate_n_90(tile, 2)
assert ["24", "13"] == rotate_n_90(tile, 3)


def flip_horizontal(tile):
    return list(map(lambda x: "".join(x[::-1]), tile))


def flip_vertical(tile):
    return transpose(flip_horizontal(transpose(tile)))


tile_by_index = dict()
with open("input_20.txt") as f:
    chunks = f.read().split("\n\n")
    for chunk in chunks:
        if not chunk.strip():
            continue
        lines = chunk.splitlines()
        tile_id = int(re.findall("\d+", lines[0])[0])
        tile_by_index[tile_id] = lines[1:]

from collections import defaultdict

side_map = defaultdict(set)

for index, tile in tile_by_index.items():
    for flip in (False, True):
        flipped_tile = flip_horizontal(tile) if flip else copy(tile)
        flipped_tile = copy(tile)
        for n in range(0, 4):
            rotated = rotate_n_90(flipped_tile, n)
            for direction in ("N", "S", "W", "E"):
                side_map[get_side(rotated, direction)].add(index)

count_unmatching_sides = defaultdict(int)
corners = set()

for side, matches in side_map.items():
    if len(matches) == 1:
        matching_side_id = list(matches)[0]
        count_unmatching_sides[matching_side_id] += 1
        if count_unmatching_sides[matching_side_id] == 4:
            corners.add(matching_side_id)
print("Part 1 answer:", prod(corners))

# Part 2


def transform_and_match(tile, side, direction):
    for flip in (False, True):
        if flip:
            flipped_tile = flip_horizontal(tile)
        else:
            flipped_tile = copy(tile)
        for n in range(0, 4):
            rotated = rotate_n_90(flipped_tile, n)
            if rotated[0] == side:
                if direction == "N":
                    return rotated
                if direction == "E":
                    return rotate_90(rotated)
                if direction == "W":
                    return transpose(rotated)
                if direction == "S":
                    return flip_vertical(rotated)
    return None


def connect_tiles(tile1, tile2, direction):
    if direction == "W":
        return list(map(lambda x: x[1] + x[0], zip(tile1, tile2)))
    if direction == "E":
        return list(map(lambda x: x[0] + x[1], zip(tile1, tile2)))
    if direction == "S":
        return tile1 + tile2
    if direction == "N":
        return tile2 + tile1


def strip_tile(tile):
    return list(map(lambda x: x[1:-1], tile[1:-1]))


opposite_direction_map = {"N": "S", "S": "N", "E": "W", "W": "E"}

puzzle_map = defaultdict(dict)
corner_id = list(corners)[0]
tile = tile_by_index[corner_id]
unseen_tile_ids_and_directions = list(
    map(lambda x: (corner_id, tile, x), ("N", "S", "E", "W"))
)
# direction means that the next tile's adjacent side is "N" or "W"

while unseen_tile_ids_and_directions:
    tile_id, tile, direction = unseen_tile_ids_and_directions.pop()
    side = get_side(tile, direction)
    adjacent_ids = side_map[side]

    if len(adjacent_ids) == 1:
        continue
    neighbor_tile_id = [id_ for id_ in side_map[side] if id_ != tile_id][0]

    opposite_direction = opposite_direction_map[direction]

    neighbor_tile = tile_by_index[neighbor_tile_id]
    transformed_neighbor_tile = transform_and_match(
        neighbor_tile, side, opposite_direction
    )

    if transformed_neighbor_tile:
        puzzle_map[tile_id][direction] = (neighbor_tile_id, transformed_neighbor_tile)
        for add_direction in ["N", "S", "E", "W"]:
            if add_direction == opposite_direction:
                continue
            if not puzzle_map.get(neighbor_tile_id, {}).get(add_direction):
                unseen_tile_ids_and_directions.append(
                    (neighbor_tile_id, transformed_neighbor_tile, add_direction)
                )


filtered_directions = puzzle_map[corner_id].keys()

vertical_direction = "N" if "N" in filtered_directions else "S"
horizontal_chunks = [(corner_id, tile_by_index[corner_id])]

while True:
    neighbor_tile_id, neighbor_tile = puzzle_map[horizontal_chunks[-1][0]].get(
        vertical_direction, (None, None)
    )
    if not neighbor_tile_id:
        break
    else:
        horizontal_chunks.append((neighbor_tile_id, neighbor_tile))

horizontal_direction = "W" if "W" in filtered_directions else "E"

image = []

for horizontal_chunk_id, initial_tile in horizontal_chunks:
    chunk_image = strip_tile(initial_tile)
    tile_id = horizontal_chunk_id
    while True:
        neighbor_tile_id, neighbor_tile = puzzle_map[tile_id].get(
            horizontal_direction, (None, None)
        )
        if not neighbor_tile_id:
            image = connect_tiles(image, chunk_image, vertical_direction)
            break
        else:
            chunk_image = connect_tiles(
                chunk_image, strip_tile(neighbor_tile), horizontal_direction
            )
            tile_id = neighbor_tile_id


monster = ["                  # ", "#    ##    ##    ###", " #  #  #  #  #  #   "]
monster_regexes = list(map(lambda x: x.replace(" ", "."), monster))


def test_lines_for_monster(lines):
    for index, monster_regex in enumerate(monster_regexes):
        if not re.findall(monster_regex, lines[index]):
            return False
    return True


test_monster = [
    ".#...#.###...#.##.##.",
    "#.##.###.#.##.##.####",
    "##.###.####..#.####.#",
]
assert test_lines_for_monster(test_monster)


def test_image_for_monster(image):
    monsters_count = 0
    for line_index in range(len(image) - len(monster) + 1):
        for start in range(len(image[0]) - len(monster[0]) + 1):
            monster_candidate = [
                image[line_index + index][start : len(monster[0]) + start]
                for index in range(3)
            ]
            dim_candidate = list(map(len, monster_candidate))
            dim_monster = list(map(len, monster))
            assert dim_monster == dim_candidate
            if test_lines_for_monster(monster_candidate):
                monsters_count += 1
    return monsters_count


test_image = [
    "..#...#.###...#.##.##.",
    ".#.##.###.#.##.##.####",
    ".##.###.####..#.####.#",
]

assert 1 == test_image_for_monster(test_image)


test_image = [
    ".####...#####..#...###..",
    "#####..#..#.#.####..#.#.",
    ".#.#...#.###...#.##.##..",
    "#.#.##.###.#.##.##.#####",
    "..##.###.####..#.####.##",
    "...#.#..##.##...#..#..##",
    "#.##.#..#.#..#..##.#.#..",
    ".###.##.....#...###.#...",
    "#.####.#.#....##.#..#.#.",
    "##...#..#....#..#...####",
    "..#.##...###..#.#####..#",
    "....#.##.#.#####....#...",
    "..##.##.###.....#.##..#.",
    "#...#...###..####....##.",
    ".#.##...#.##.#.#.###...#",
    "#.###.#..####...##..#...",
    "#.###...#.##...#.######.",
    ".###.###.#######..#####.",
    "..##.#..#..#.#######.###",
    "#.#..##.########..#..##.",
    "#.#####..#.#...##..#....",
    "#....##..#.#########..##",
    "#...#.....#..##...###.##",
    "#..###....##.#...##.##.#",
]

assert 2 == test_image_for_monster(test_image)


max_monsters_count = 0

for flip in (False, True):
    flipped_image = flip_horizontal(image) if flip else copy(image)
    for n in range(0, 4):
        flipped_image = rotate_n_90(flipped_image, n)
        monsters_count = test_image_for_monster(flipped_image)
        if monsters_count > max_monsters_count:
            max_monsters_count = monsters_count

# Assuming that monsters do not overlap
print(
    "Part 2 answer:",
    sum(line.count("#") for line in image)
    - max_monsters_count * sum(line.count("#") for line in monster),
)
