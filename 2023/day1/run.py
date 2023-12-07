from pathlib import Path

LETTER_DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

REVERSED_LETTER_DIGITS = {key[::-1]: value for key, value in LETTER_DIGITS.items()}


def read_calibration(file_path, advanced=False):
    if advanced:
        read_first_digit_ = lambda x: read_first_digit_advanced(x, LETTER_DIGITS)
        read_last_digit_ = lambda x: read_first_digit_advanced(x[::-1], REVERSED_LETTER_DIGITS)

    else:
        read_first_digit_ = read_first_digit
        read_last_digit_ = lambda x: read_first_digit(x[::-1])

    calibration_sum = 0
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                calibration = read_first_digit_(line) + read_last_digit_(line)
                calibration_sum += int(calibration)

    return calibration_sum


def read_first_digit(string):
    for char in string:
        if char.isdigit():
            return char


def read_first_digit_advanced(string, valid_letter_digits):
    pointer = 0

    while pointer < len(string):
        char = string[pointer]
        if char.isdigit():
            return char

        pointer_exclusiv_word_end = 1
        pool_of_letters = list(valid_letter_digits.keys())

        while pool_of_letters:
            if pool_of_letters[-1].startswith(string[pointer : pointer + pointer_exclusiv_word_end]):
                if len(pool_of_letters[-1]) == pointer_exclusiv_word_end:
                    return str(valid_letter_digits[pool_of_letters[-1]])

                pointer_exclusiv_word_end += 1
            else:
                pool_of_letters.pop()
        pointer += 1


if __name__ == "__main__":
    file_path = Path(__file__).parent.joinpath("example1.txt")

    calibration_sum = read_calibration(file_path, advanced=False)
    print(calibration_sum)

    file_path = Path(__file__).parent.joinpath("example2.txt")

    calibration_sum = read_calibration(file_path, advanced=True)
    print(calibration_sum)
