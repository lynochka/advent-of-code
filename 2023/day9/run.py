from pathlib import Path


def read_lines_from_file(file_path):
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            yield line


def analyse_oasis(file_path, reverse_=False):
    lines = list(read_lines_from_file(file_path))
    sum_ = 0
    for line in lines:
        sum_ += predict_history(line, reverse_)
    print("Sum", sum_)


def predict_history(line, reverse_):
    sequence = list(map(int, line.split(" ")))
    differences = [sequence]
    while True:
        difference = list(map(lambda x, y: y - x, sequence[:-1], sequence[1:]))

        differences.append(difference)
        sequence = [d for d in difference]
        if all([d == 0 for d in difference]):
            if reverse_:
                difference.insert(0, 0)
            else:
                difference.append(0)
            break

    left = None
    child = None
    for index in range(1, len(differences))[::-1]:
        if reverse_:
            child = differences[index][0]
            left = differences[index - 1][0]
            right = left - child
            differences[index - 1].insert(0, right)
        else:
            child = differences[index][-1]
            left = differences[index - 1][-1]
            right = left + child
            differences[index - 1].append(right)
    return right


if __name__ == "__main__":
    file_path = Path(__file__).parent.joinpath("input.txt")

    analyse_oasis(file_path)

    analyse_oasis(file_path, True)
