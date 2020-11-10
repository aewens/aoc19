package solutions

func init() {
	Map[3] = Solution3
}

type Point struct {
	X int
	Y int
}

type Cabling struct {
	Closest int
	Grid    map[Point][]int
}

func abs(x int) int {
	if x < 0 {
		return -x
	}

	return x
}

func push(xs []int, y int) []int {
	for _, x := range xs {
		if x == y {
			return xs
		}
	}

	return append(xs, y)
}

func getDistance(point Point) int {
	return abs(point.X) + abs(point.Y)
}

func checkPoint(cabling *Cabling, point Point) {
	if len(cabling.Grid[point]) > 1 {
		distance := getDistance(point)
		if cabling.Closest == -1 {
			cabling.Closest = distance
		} else {
			if distance < cabling.Closest {
				cabling.Closest = distance
			}
		}
	}
}

func PlotWire(cabling *Cabling, instructions []string, w int) {
	x, y := 0, 0
	for _, instruction := range instructions {
		steps := StringToInt(instruction[1:])

		for step := 0; step < steps; step++ {
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

			point := Point{x, y}
			cabling.Grid[point] = push(cabling.Grid[point], w)
			checkPoint(cabling, point)
		}
	}
}

func Solution3(lines chan string) {
	wire := 0
	cabling := &Cabling{
		Closest: -1,
		Grid:    make(map[Point][]int),
	}

	for line := range lines {
		wire = wire + 1
		instructions := FromCSV(line)
		PlotWire(cabling, instructions, wire)
	}

	Display(1, cabling.Closest)
}
