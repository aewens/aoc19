package solutions

import (
	"github.com/aewens/aoc19/pkg/utilities"
)

func init() {
	Map[4] = Solution4
}

func hasRepeats(check rune, seen map[rune]bool) bool {
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

func ValidGuess(guess int) []bool {
	seen := make(map[rune]bool)
	doubles := make(map[rune]bool)
	previous := -1
	prevPrevious := -1

	repeats := false
	decreases := false
	double := false

	guessString := utilities.IntToString(guess)
	for _, gs := range guessString {
		if hasRepeats(gs, seen) {
			if !repeats {
				repeats = true
			}

			double = true
			doubles[gs] = true
		}

		gsi := utilities.RuneToInt(gs)
		if doesDecrease(gsi, previous) {
			decreases = true
			continue
		}

		if gsi == previous && previous == prevPrevious && doubles[gs] {
			doubles[gs] = false
			double = false
			for _, isDouble := range doubles {
				if isDouble {
					double = true
					break
				}
			}
		}

		if previous != -1 {
			prevPrevious = previous
		}
		previous = gsi
	}

	valid1 := repeats && !decreases
	valid2 := valid1 && double
	return []bool{valid1,valid2}
}

func Solution4(lines chan string) {
	passwordRange := Separate(<-lines, "-")
	rangeStart := utilities.StringToInt(passwordRange[0])
	rangeEnd := utilities.StringToInt(passwordRange[1])

	validGuesses := []int{0,0}
	for guess := rangeStart; guess <= rangeEnd; guess++ {
		valid := ValidGuess(guess)

		if valid[0] {
			validGuesses[0] = validGuesses[0] + 1
		}

		if valid[1] {
			validGuesses[1] = validGuesses[1] + 1
		}
	}

	Display(1, validGuesses[0])
	Display(2, validGuesses[1])
}
