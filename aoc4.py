
def get_valid_passwords(puzzle_input, limit_adjacents=False):
    start, end = puzzle_input.split("-")
    password_range = map(str, range(int(start), int(end)))
    valid_passwords = list()

    for test_case in password_range:
        adjacent = False
        decreases = False
        previous = str(-1)
        adjacents = dict()

        for index in range(len(test_case)):
            digit = test_case[index]
            if digit == previous:
                adjacent = True
                if limit_adjacents:
                    adjacents[digit] = adjacents.get(digit, 0) + 1

            if int(digit) < int(previous):
                decreases = True
                break

            previous = digit

        if not decreases and adjacent:
            if limit_adjacents:
                if 1 in adjacents.values():
                    valid_passwords.append(test_case)

            else:
                valid_passwords.append(test_case)

    return valid_passwords

if __name__ == "__main__":
    puzzle_input = "240920-789857"
    valid_passwords1 = get_valid_passwords(puzzle_input)
    print("Part 1:", len(valid_passwords1))

    valid_passwords2 = get_valid_passwords(puzzle_input, True)
    print("Part 2:", len(valid_passwords2))
