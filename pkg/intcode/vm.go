package intcode

import (
	"fmt"
	"strings"
	"strconv"
)

type Computer struct {
	Position int
	Codes    []int
	Memory   []int
}

//func debug(computer *Computer) {
//	opcode := computer.Memory[computer.Position]
//	arg1 := computer.Memory[computer.Position + 1]
//	arg2 := computer.Memory[computer.Position + 2]
//	arg3 := computer.Memory[computer.Position + 3]
//	fmt.Printf("[*] %d | %d %d %d\n", opcode, arg1, arg2, arg3)
//}

func checkBounds(computer *Computer, offset int) {
	position := computer.Position + offset
	if position < 0 || position >= len(computer.Memory) {
		panic(fmt.Sprintf("Index %d is out of bounds", position))
	}
}

func readWrite(computer *Computer, operation func(int, int) int) {
	checkBounds(computer, 1)
	read1 := computer.Memory[computer.Position+1]
	value1 := computer.Memory[read1]

	checkBounds(computer, 2)
	read2 := computer.Memory[computer.Position+2]
	value2 := computer.Memory[read2]

	checkBounds(computer, 3)
	write := computer.Memory[computer.Position+3]
	computer.Memory[write] = operation(value1, value2)
}

func save(original []int) []int {
	backup := make([]int, len(original))
	copy(backup, original)
	return backup
}

func Parser(program string) []int {
	var codes []int

	instructions := strings.Split(program, ",")
	for _, instruction := range instructions {
		code, err := strconv.Atoi(instruction)
		if err != nil {
			panic(err)
		}
		codes = append(codes, code)
	}

	return codes
}

func New(program string) *Computer {
	codes := Parser(program)
	memory := save(codes)

	return &Computer{
		Position: 0,
		Codes:    codes,
		Memory:   memory,
	}
}

func (computer *Computer) Reset() {
	computer.Position = 0
	computer.Memory = save(computer.Codes)
}

func (computer *Computer) Load(program string) {
	computer.Codes = Parser(program)
	computer.Reset()
}

func (computer *Computer) Run() []int {
	halt := false

	for {
		checkBounds(computer, 0)
		opcode := computer.Memory[computer.Position]

		switch opcode {
		case 1:
			//debug(computer)
			readWrite(computer, func(a int, b int) int {
				return a + b
			})

		case 2:
			//debug(computer)
			readWrite(computer, func(a int, b int) int {
				return a * b
			})

		case 99:
			halt = true

		default:
			panic(fmt.Sprintf("Invalid opcode: %d", opcode))
		}

		if halt {
			break
		}

		computer.Position = computer.Position + 4
	}

	return computer.Memory
}
