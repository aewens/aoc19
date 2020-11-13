package solutions

import (
	"github.com/aewens/aoc19/pkg/intcode"
)

func init() {
	Map[5] = Solution5
}

func Solution5(lines chan string) {
	computer := intcode.BufferedNew(<-lines)

	go func() {
		solution := 1
		computer.InBuffer <- 1
		for output := range computer.OutBuffer {
			Display(solution, output)
			if output != 0 {
				solution = 2
				computer.InBuffer <- 5
			}
		}
	}()

	computer.Run()
	computer.Reset()
	computer.Run()

}
