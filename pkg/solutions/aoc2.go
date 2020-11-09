package solutions

import (
	"github.com/aewens/aoc19/pkg/intcode"
)

func init() {
	Map[2] = Solution2
}

func Solution2(lines chan string) {
	for line := range lines {
		computer := intcode.New(line)
		computer.Memory[1] = 12
		computer.Memory[2] = 2

		codes := computer.Run()
		Display(1, codes[0])

		searching := true
		for verb := 0; verb <= 99; verb++ {
			if !searching {
				break
			}
			for noun := 0; noun <= 99; noun++ {
				computer.Reset()
				computer.Memory[1] = noun
				computer.Memory[2] = verb

				output := computer.Run()[0]
				if output == 19690720 {
					searching = false
					Display(2, 100 * noun + verb)
					break
				}
			}
		}
	}
}
