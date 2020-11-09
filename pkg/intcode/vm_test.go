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

func TestCompute(t *testing.T) {
	defer Cleanup(t)

	program1 := "1,9,10,3,2,3,11,0,99,30,40,50"
	codes1 := Compute(program1)

	if codes1[0] != 3500 {
		t.Fatal("Program 1 was read incorrectly")
	}

	program2 := "2,3,0,3,99"
	codes2 := Compute(program2)

	if codes2[3] != 6 {
		t.Fatal("Program 2 was read incorrectly")
	}

	program3 := "2,4,4,5,99,0"
	codes3 := Compute(program3)

	if codes3[5] != 9801 {
		t.Fatal("Program 3 was read incorrectly")
	}

	program4 := "1,1,1,4,99,5,6,0,99"
	codes4 := Compute(program4)

	if codes4[0] != 30 {
		t.Fatal("Program 4 was read incorrectly")
	}
}
