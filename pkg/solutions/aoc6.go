package solutions

//import (
//	"github.com/aewens/aoc19/pkg/utilities"
//)

func init() {
	Map[6] = Solution6
}

type OrbitMap struct {
	Forward  map[string][]string
	Backward map[string]string
}

func BuildOrbitMap(orbits *OrbitMap, orbitPair string) {
	pair := Separate(orbitPair, ")")
	head := pair[0]
	tail := pair[1]

	orbits.Backward[tail] = head

	_, ok := orbits.Forward[head]
	if !ok {
		orbits.Forward[head] = []string{tail}
	} else {
		orbits.Forward[head] = append(orbits.Forward[head], tail)
	}
}

func CountOrbits(orbits *OrbitMap, body string, total int) int {
	switch body {
	case "":
		for _, body := range orbits.Backward {
			total = CountOrbits(orbits, body, total+1)
		}
	case "COM":
		return total
	default:
		return CountOrbits(orbits, orbits.Backward[body], total+1)
	}

	return total
}

func Solution6(lines chan string) {
	orbits := &OrbitMap{
		Forward:  make(map[string][]string),
		Backward: make(map[string]string),
	}

	for line := range lines {
		BuildOrbitMap(orbits, line)
	}

	Display(1, CountOrbits(orbits, "", 0))
}
