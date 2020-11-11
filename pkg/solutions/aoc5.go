package solutions

import (
	"github.com/aewens/aoc19/pkg/intcode"
)

func init() {
	Map[5] = Solution5
}

func Solution5(lines chan string) {
	computer := intcode.New(<-lines)
	//codes := computer.Run()
	//Display(1, codes)
	computer.Run()
}
