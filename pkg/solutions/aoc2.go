package solutions

import (
	"github.com/aewens/aoc19/pkg/intcode"
)

func init() {
	Map[2] = Solution2
}

func Solution2(lines chan string) {
	for line := range lines {
		program := intcode.Parser(line)
		program[1] = 12
		program[2] = 2

		codes := intcode.Reader(program)
		Display(1, codes[0])
	}
}
