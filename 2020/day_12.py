import math
from copy import copy

#     N
#     |
# W - . - E
#     |
#     S

# Part 1

face_angle_map = {"E": 0, "N": 90, "W": 180, "S": 270}
angle_face_map = {v: k for k, v in face_angle_map.items()}

face_direction_map = {"E": (1, 0), "N": (0, 1), "W": (-1, 0), "S": (0, -1)}


def move(lines):
    """
    Move according to line instructions, return Manhattan distance.
    """
    face = "E"
    coordinate = [0, 0]
    for line in lines:
        action = line[0]
        value = int(line[1:])
        if action in face_direction_map:
            direction = face_direction_map[action]
            for index in range(2):
                coordinate[index] += direction[index] * value
            continue

        if action in ("L", "R"):
            sign = -1 if action == "R" else 1
            face = angle_face_map[(face_angle_map[face] + sign * value) % 360]
            continue

        if action == "F":
            direction = face_direction_map[face]
            for index in range(2):
                coordinate[index] += direction[index] * value
    return sum(map(abs, coordinate))


sample_lines = """F10
N3
F7
R90
F11""".split(
    "\n"
)
assert 25 == move(sample_lines)

with open("input_12.txt") as f:
    lines = f.readlines()
print("Manhattan distance =", move(lines))

# Part 2


def rotate_around_origin(coordinate, angle, decimal_number=6):
    radian_angle = 2 * math.pi * angle / 360
    x = coordinate[0]
    y = coordinate[1]
    x1 = x * math.cos(radian_angle) - y * math.sin(radian_angle)
    y1 = y * math.cos(radian_angle) + x * math.sin(radian_angle)
    return [round(x1, decimal_number), round(y1, decimal_number)]


assert [0, 2] == rotate_around_origin((2, 0), 90)


# This should have been used instead for rotation to my opnion
def rotate_around_point(coordinate, angle, point):
    new_coordinate = copy(list(coordinate))
    for index in range(2):
        new_coordinate[index] -= point[index]
    new_coordinate = rotate_around_origin(new_coordinate, angle)
    for index in range(2):
        new_coordinate[index] += point[index]
    return new_coordinate


assert [0, 3] == rotate_around_point((1, 2), 90, (0, 2))


def move_with_waypoint(lines):
    """
    Move according to line instructions, return Manhattan distance.
    """
    waypoint = [10, 1]
    coordinate = [0, 0]
    for line in lines:
        action = line[0]
        value = int(line[1:])
        if action == "F":
            for index in range(2):
                coordinate[index] += waypoint[index] * value
            continue

        if action in face_direction_map:
            direction = face_direction_map[action]
            for index in range(2):
                waypoint[index] += direction[index] * value
            continue

        if action in ("L", "R"):
            sign = -1 if action == "R" else 1
            waypoint = rotate_around_origin(waypoint, sign * value)
            continue

    return sum(map(abs, coordinate))


assert 286 == move_with_waypoint(sample_lines)

print("Manhattan distance (with waypoint)  =", move_with_waypoint(lines))
