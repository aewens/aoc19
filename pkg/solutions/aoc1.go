package solutions

import (
	"github.com/aewens/aoc19/pkg/utilities"
)

func init() {
	Map[1] = Solution1
}

func getFuel(mass int) int {
	return (mass / 3) - 2
}

func getFuelFuel(fuel int) int {
	needed := getFuel(fuel)
	if needed <= 0 {
		return 0
	}

	return needed + getFuelFuel(needed)
}

func Solution1(lines chan string) {
	fuel := 0
	moduleFuel := 0
	for line := range lines {
		mass := utilities.StringToInt(line)
		neededFuel := getFuel(mass)
		fuelFuel := getFuelFuel(neededFuel)

		moduleFuel = moduleFuel + neededFuel
		fuel = fuel + fuelFuel

		if lines == nil {
			break
		}
	}
	
	Display(1, moduleFuel)
	Display(2, moduleFuel + fuel)
}
