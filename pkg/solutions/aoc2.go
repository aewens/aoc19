package solutions

import (
	"github.com/aewens/aoc19/pkg/intcode"
)

func init() {
	Map[2] = Solution2
}

func save(original []int) []int {
	backup := make([]int, len(original))
	for o := range original {
		backup[o] = original[o]
	}
	return backup
}

func Solution2(lines chan string) {
	for line := range lines {
		program := intcode.Parser(line)
		backup := save(program)

		program[1] = 12
		program[2] = 2

		codes := intcode.Reader(program)
		Display(1, codes[0])

		searching := true
		for verb := 0; verb <= 99; verb++ {
			if !searching {
				break
			}
			for noun := 0; noun <= 99; noun++ {
				program = save(backup)
				program[1] = noun
				program[2] = verb

				output := intcode.Reader(program)[0]
				if output == 19690720 {
					searching = false
					Display(2, 100 * noun + verb)
					break
				}
			}
		}
	}
}
