import re

# Part 1


def do_simple_math(expression):
    expression = expression.replace("*", "@")

    operator = "@"
    total = 1
    for value in re.findall("\d+|\+|@", expression):
        if value.isnumeric():
            if operator == "@":
                total *= int(value)
            elif operator == "+":
                total += int(value)
        if value in ("@", "+"):
            operator = value
    return total


expression = "2+11*2"
assert 26 == do_simple_math(expression)


def find_first_paranthesis(expression):
    left = 0
    right = 0
    left_most_index = None
    right_most_index = None
    for index, char in enumerate(expression):
        if char == "(":
            if left == 0:
                left_most_index = index
            left += 1
            continue
        if char == ")":
            right_most_index = index
            right += 1
        if left > right:
            continue
        if right > left:
            raise RuntimeError("Invalid expression")
        if left > 0 and left == right:
            return left_most_index, right_most_index
    return None


expression = "1 + 6 + (4 * (5 + 6))"
m = find_first_paranthesis(expression)
assert "(4 * (5 + 6))" == expression[m[0] : m[1] + 1]


def do_math(expression, simple_math_func=do_simple_math):
    m = find_first_paranthesis(expression)
    if m:
        start, end = m
        sub_expression = expression[start + 1 : end]
        result = do_math(sub_expression, simple_math_func)
        expression = expression[:start] + str(result) + expression[end + 1 :]
        return do_math(expression, simple_math_func)
    else:
        return simple_math_func(expression)


expression = "1 + (2 * 3) + (4 * (5 + 6))"
assert 51 == do_math(expression)


sum_ = 0
with open("input_18.txt") as f:
    for line in f.readlines():
        sum_ += do_math(line.strip())
print(sum_)


# ### Part 2


def do_sum_first(expression):
    m = expression.find("*")
    if m != -1:
        return do_sum_first(expression[:m]) * do_sum_first(expression[m + 1 :])
    else:
        return do_simple_math(expression)


expression = "3*2+2"
assert 12 == do_sum_first(expression)


expression = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
assert 23340 == do_math(expression, simple_math_func=do_sum_first)


sum_ = 0
with open("input_18.txt") as f:
    for line in f.readlines():
        sum_ += do_math(line.strip(), simple_math_func=do_sum_first)
print(sum_)
