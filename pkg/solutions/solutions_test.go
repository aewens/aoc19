package solutions

import (
	"testing"
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

	distances := []int{6,159,135}
	steps := []int{30,610,410}

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

	if !ValidGuess(111111) {
		t.Fatal("Not checking correctly: 111111")
	}

	if ValidGuess(223450) {
		t.Fatal("Not checking correctly: 223450")
	}

	if ValidGuess(123789) {
		t.Fatal("Not checking correctly: 123789")
	}
}
