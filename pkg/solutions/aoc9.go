package solutions

import (
	"github.com/aewens/aoc19/pkg/intcode"
)

func init() {
	Map[9] = Solution9
}

func Solution9(lines chan string) {
	program := <-lines
	computer := intcode.BufferedNew(program)
	go computer.Run()

	go computer.Input(1)
	Display(1, computer.Output())
}
