import re
from pathlib import Path
from collections import defaultdict
from functools import reduce


def read_lines_from_file(file_path):
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            yield line


def count_points(file_path):
    sum_ = 0
    for line in read_lines_from_file(file_path):
        _, count_guessed_right = count_card_guessed_right(line)
        points = 2 ** (count_guessed_right - 1) if count_guessed_right > 0 else 0
        sum_ += points
    print("Sum points:", sum_)


def count_card_guessed_right(line):
    match = re.search("Card\s+(\d+):(.+)\|(.+)", line)
    card_index = match.group(1)
    winning_numbers = set(map(int, match.group(2).split()))
    guessed_numbers = set(map(int, match.group(3).split()))
    count_guessed_right = len(guessed_numbers.intersection(winning_numbers))
    return card_index, count_guessed_right


def count_cards_with_copies(file_path):
    card_index_points = list()
    for line in read_lines_from_file(file_path):
        card_index, count_guessed_right = count_card_guessed_right(line)
        card_index_points.append((card_index, count_guessed_right))

    card_copies = defaultdict(int)
    for order_index, (card_index, count_guessed_right) in enumerate(card_index_points):
        for copy_order_index in range(order_index + 1, order_index + count_guessed_right + 1):
            if copy_order_index >= len(card_index_points):
                break
            copied_card_index = card_index_points[copy_order_index][0]
            card_copies[copied_card_index] += 1 + card_copies.get(card_index, 0)
    print("# cards with copies:", reduce(lambda x, y: x + y, card_copies.values()) + len(card_index_points))


if __name__ == "__main__":
    file_path = Path(__file__).parent.joinpath("input.txt")
    count_points(file_path)

    count_cards_with_copies(file_path)
