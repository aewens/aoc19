package solutions

func init() {
	Map[4] = Solution4
}

func hasDoubles(check rune, seen map[rune]bool) bool {
	_, ok := seen[check]
	if ok {
		return true
	}

	seen[check] = true
	return false
}

func doesDecrease(check int, previous int) bool {
	return check < previous
}

func ValidGuess(guess int) bool {
	seen := make(map[rune]bool)
	previous := -1

	doubles := false
	decreases := false

	guessString := IntToString(guess)
	for _, gs := range guessString {
		if !doubles && hasDoubles(gs, seen) {
			doubles = true
		}

		gsi := RuneToInt(gs)
		if doesDecrease(gsi, previous) {
			decreases = true
			continue
		}

		previous = gsi
	}

	return doubles && !decreases
}

func Solution4(lines chan string) {
	passwordRange := Separate(<-lines, "-")
	rangeStart := StringToInt(passwordRange[0])
	rangeEnd := StringToInt(passwordRange[1])

	validGuesses := 0
	for guess := rangeStart; guess <= rangeEnd; guess++ {
		if ValidGuess(guess) {
			validGuesses = validGuesses + 1
		}
	}

	Display(1, validGuesses)
}
