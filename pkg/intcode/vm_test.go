package intcode

import (
	"testing"
)

func Cleanup(t *testing.T) {
	r := recover()
	if r != nil {
		t.Fatal(r)
	}
}

func TestParser(t *testing.T) {
	defer Cleanup(t)

	program := "1,9,10,3,2,3,11,0,99,30,40,50"
	codes := Parser(program)

	correctCodes := []int{1,9,10,3,2,3,11,0,99,30,40,50}

	if len(codes) != len(correctCodes) {
		t.Fatal("Program was parsed to the wrong size")
	}

	for c, code := range codes {
		correctCode := correctCodes[c]
		if code != correctCode {
			t.Fatal("Program was not parsed correctly")
		}
	}
}

func TestReadOpcode(t *testing.T) {
	defer Cleanup(t)

	computer := New("1,9,10,11,1102,2,3,12,99,2,3,-1,-1")
	codes := computer.Run()

	if codes[11] != 5 {
		t.Fatal("Did not process first opcode correctly")
	}

	if codes[12] != 6 {
		t.Fatal("Did not process second opcode correctly")
	}

}

func TestComputer(t *testing.T) {
	defer Cleanup(t)

	computer := New("1,9,10,3,2,3,11,0,99,30,40,50")
	codes := computer.Run()
	if codes[0] != 3500 {
		t.Fatal("Program 1 was read incorrectly")
	}

	programs := []string{
		"2,3,0,3,99",
		"2,4,4,5,99,0",
		"1,1,1,4,99,5,6,0,99",
		"1101,100,-1,4,0,99",
		"8,5,6,7,99,8,8,-1",
		"7,5,6,7,99,8,8,-1",
		"1108,8,8,5,99,-1",
		"1107,8,8,5,99,-1",
		"1107,8,8,5,99,-1",
		"6,8,11,1,9,10,9,99,0,0,1,7",
		"6,8,11,1,9,10,9,99,1,0,1,7",
		"1105,1,7,1101,0,0,8,99,1",
	}

	results := [][]int{
		[]int{3,6},
		[]int{5,9801},
		[]int{0,30},
		[]int{4,99},
		[]int{7,1},
		[]int{7,0},
		[]int{5,1},
		[]int{5,0},
		[]int{5,0},
		[]int{9,0},
		[]int{9,1},
		[]int{8,1},
		[]int{8,0},
	}

	for p, program := range programs {
		computer.Load(program)
		codes = computer.Run()
		result := results[p]
		if codes[result[0]] != result[1] {
			t.Fatalf("Program %d was read incorrectly", p + 2)
		}
	}
}
