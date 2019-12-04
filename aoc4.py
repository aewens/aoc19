
def get_valid_passwords(puzzle_input):
    start, end = puzzle_input.split("-")
    password_range = map(str, range(int(start), int(end)))
    valid_passwords = list()

    for test_case in password_range:
        adjacent = False
        decreases = False
        previous = str(-1)

        for index in range(len(test_case)):
            digit = test_case[index]
            if not adjacent and digit == previous:
                adjacent = True

            if int(digit) < int(previous):
                decreases = True
                break

            previous = digit

        if not decreases and adjacent:
            valid_passwords.append(test_case)

    return valid_passwords

if __name__ == "__main__":
    puzzle_input = "240920-789857"
    valid_passwords = get_valid_passwords(puzzle_input)
    print("Part 1:", len(valid_passwords))
