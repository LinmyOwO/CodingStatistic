from random import randint


def generate_number(digits=3, left=None, right=None):
    if not left:
        left = 0
    if not right:
        right = 10 ** digits - 1

    number = randint(left, right)
    return number


def generate_unique_array(amount, digits=3, left=None, right=None):
    arr = []
    unique_check_set = set()
    i = 0
    while i < amount:
        number = generate_number(digits, left, right)
        if number not in unique_check_set:
            arr.append(number)
            i += 1
    return arr
