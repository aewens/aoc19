package solutions

import (
	"testing"
	"strings"
)

func Cleanup(t *testing.T) {
	r := recover()
	if r != nil {
		t.Fatal(r)
	}
}

func TestPlotWire(t *testing.T) {
	defer Cleanup(t)

	var tests [][]string
	tests = append(tests, []string{
		"R8,U5,L5,D3",
		"U7,R6,D4,L4",
	})
	tests = append(tests, []string{
		"R75,D30,R83,U83,L12,D49,R71,U7,L72",
		"U62,R66,U55,R34,D71,R55,D58,R83",
	})
	tests = append(tests, []string{
		"R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
		"U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
	})

	distances := []int{6, 159, 135}
	steps := []int{30, 610, 410}

	for i, test := range tests {
		wire := 0
		cabling := &Cabling{
			ClosestOrigin: -1,
			ClosestSignal: -1,
			Grid:          make(map[Point][][]int),
		}

		for _, path := range test {
			wire = wire + 1
			instructions := FromCSV(path)
			PlotWire(cabling, instructions, wire)
		}

		distance := distances[i]
		if distance != cabling.ClosestOrigin {
			t.Fatalf("Wrong distance: %d | %d", distance, cabling.ClosestOrigin)
		}

		step := steps[i]
		if step != cabling.ClosestSignal {
			t.Fatalf("Wrong step: %d | %d", step, cabling.ClosestSignal)
		}
	}
}

func TestValidGuess(t *testing.T) {
	defer Cleanup(t)

	if !ValidGuess(111111)[0] {
		t.Fatal("Not checking correctly: 111111")
	}

	if ValidGuess(223450)[0] {
		t.Fatal("Not checking correctly: 223450")
	}

	if ValidGuess(123789)[0] {
		t.Fatal("Not checking correctly: 123789")
	}

	if !ValidGuess(112233)[1] {
		t.Fatal("Not checking correctly: 112233")
	}

	if ValidGuess(123444)[1] {
		t.Fatal("Not checking correctly: 123444")
	}

	if !ValidGuess(111122)[1] {
		t.Fatal("Not checking correctly: 111122")
	}
}

func TestCountOrbits(t *testing.T) {
	orbits := make(OrbitMap)

	pairs := []string{
		"COM)B",
		"B)C",
		"C)D",
		"D)E",
		"E)F",
		"B)G",
		"G)H",
		"D)I",
		"E)J",
		"J)K",
		"K)L",
	}

	for _, pair := range pairs {
		BuildOrbitMap(orbits, pair)
	}

	count := CountOrbits(orbits, "", 0)
	if count != 42 {
		t.Fatalf("Count orbits is incorrect: %d", count)
	}
}

func TestFindOrbitPath(t *testing.T) {
	orbits := make(OrbitMap)

	pairs := []string{
		"COM)B",
		"B)C",
		"C)D",
		"D)E",
		"E)F",
		"B)G",
		"G)H",
		"D)I",
		"E)J",
		"J)K",
		"K)L",
		"K)YOU",
		"I)SAN",
	}

	for _, pair := range pairs {
		BuildOrbitMap(orbits, pair)
	}

	path := FindOrbitPath(orbits, "YOU", "SAN")
	if len(path) != len([]string{"K", "J", "E", "D", "I"}) {
		t.Fatalf("Found wrong path: %#v", path)
	}
}

func TestThrusterSignal(t *testing.T) {
	testPhases := [][]int{
		[]int{4,3,2,1,0},
		[]int{0,1,2,3,4},
		[]int{1,0,4,3,2},
	}

	testPrograms := []string{
		"3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0",
		strings.Join([]string{
			"3,23,3,24,1002,24,10,24,1002,23,-1,23",
			"101,5,23,23,1,24,23,23,4,23,99,0,0",
		}, ","),
		strings.Join([]string{
			"3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33",
			"1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
		}, ","),
	}

	testSignals := []int{43210,54321,65210}

	for p, phases := range testPhases {
		program := testPrograms[p]
		computers := CreateNetwork(program, len(phases))
		signal := ThrusterSignal(computers, phases)

		testSignal := testSignals[p]
		if signal != testSignal {
			t.Fatalf("Incorrect signal for %d: %d | %d", p, signal, testSignal)
		}
	}
}
