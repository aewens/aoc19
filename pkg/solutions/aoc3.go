package solutions

import (
	"github.com/aewens/aoc19/pkg/utilities"
)

func init() {
	Map[3] = Solution3
}

type Point struct {
	X int
	Y int
}

type Cabling struct {
	ClosestSignal int
	ClosestOrigin int
	Grid          map[Point][][]int
}

func abs(x int) int {
	if x < 0 {
		return -x
	}

	return x
}

func push(xs [][]int, y []int) [][]int {
	// Check if first index of y exists in xs
	for _, x := range xs {
		if x[0] == y[0] {
			return xs
		}
	}

	return append(xs, y)
}

func getDistance(point Point) int {
	return abs(point.X) + abs(point.Y)
}

func checkPoint(cabling *Cabling, point Point) {
	stats := cabling.Grid[point]
	if len(stats) > 1 {
		distance := getDistance(point)
		if cabling.ClosestOrigin == -1 {
			cabling.ClosestOrigin = distance
		} else if distance < cabling.ClosestOrigin {
			cabling.ClosestOrigin = distance
		}

		totalSteps := 0
		for _, stat := range stats {
			steps := stat[1]
			totalSteps = totalSteps + steps
		}

		if cabling.ClosestSignal == -1 {
			cabling.ClosestSignal = totalSteps
		} else if totalSteps < cabling.ClosestSignal {
			cabling.ClosestSignal = totalSteps
		}
	}
}

func PlotWire(cabling *Cabling, instructions []string, w int) {
	x, y, steps := 0, 0, 0
	for _, instruction := range instructions {
		length := utilities.StringToInt(instruction[1:])

		for l := 0; l < length; l++ {
			switch instruction[0] {
			case 'U':
				y = y + 1
			case 'D':
				y = y - 1
			case 'R':
				x = x + 1
			case 'L':
				x = x - 1
			default:
				panic("Invalid instruction")
			}

			steps = steps + 1
			point := Point{x, y}
			cabling.Grid[point] = push(cabling.Grid[point], []int{w, steps})
			checkPoint(cabling, point)
		}
	}
}

func Solution3(lines chan string) {
	wire := 0
	cabling := &Cabling{
		ClosestOrigin: -1,
		ClosestSignal: -1,
		Grid:          make(map[Point][][]int),
	}

	for line := range lines {
		wire = wire + 1
		instructions := FromCSV(line)
		PlotWire(cabling, instructions, wire)
	}

	Display(1, cabling.ClosestOrigin)
	Display(2, cabling.ClosestSignal)
}
