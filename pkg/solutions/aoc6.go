package solutions

func init() {
	Map[6] = Solution6
}

type OrbitMap map[string]string

func BuildOrbitMap(orbits OrbitMap, orbitPair string) {
	pair := Separate(orbitPair, ")")
	head := pair[0]
	tail := pair[1]

	orbits[tail] = head
}

func CountOrbits(orbits OrbitMap, body string, total int) int {
	switch body {
	case "":
		for _, body := range orbits {
			total = CountOrbits(orbits, body, total+1)
		}
	case "COM":
		return total
	default:
		return CountOrbits(orbits, orbits[body], total+1)
	}

	return total
}

func FindOrbitPath(orbits OrbitMap, start string, stop string) []string {
	var path []string

	startToCOM := []string{orbits[start]}
	for {
		size := len(startToCOM)
		prev := startToCOM[size-1]
		body := orbits[prev]

		if body == "COM" {
			break
		}

		startToCOM = append(startToCOM, body)
	}

	stopToCommon := []string{orbits[stop]}
	for {
		size := len(stopToCommon)
		prev := stopToCommon[size-1]
		body := orbits[prev]

		common := false
		for c, check := range startToCOM {
			if check == body {
				common = true
				path = append(startToCOM[:c+1], stopToCommon...)
				break
			}
		}

		if common {
			break
		}

		stopToCommon = append(stopToCommon, body)
	}

	return path
}

func Solution6(lines chan string) {
	orbits := make(OrbitMap)
	for line := range lines {
		BuildOrbitMap(orbits, line)
	}

	Display(1, CountOrbits(orbits, "", 0))
	Display(2, len(FindOrbitPath(orbits, "YOU", "SAN"))-1)
}
