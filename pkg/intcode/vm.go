package intcode

import (
	"fmt"
	"strings"
	"strconv"
)

func debug(codes []int, position int) {
	opcode := codes[position]
	arg1 := codes[position + 1]
	arg2 := codes[position + 2]
	arg3 := codes[position + 3]
	fmt.Printf("[*] %d | %d %d %d\n", opcode, arg1, arg2, arg3)
}

func checkBounds(codes []int, position int) {
	if position < 0 || position >= len(codes) {
		panic(fmt.Sprintf("Index %d is out of bounds", position))
	}
}

func readWrite(codes []int, position int, operation func(int, int) int) {
	checkBounds(codes, position+1)
	read1 := codes[position+1]
	value1 := codes[read1]

	checkBounds(codes, position+2)
	read2 := codes[position+2]
	value2 := codes[read2]

	checkBounds(codes, position+3)
	write := codes[position+3]
	codes[write] = operation(value1, value2)
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

func Reader(codes []int) []int {
	halt := false
	position := 0
	for {
		if halt {
			break
		}

		checkBounds(codes, position)
		opcode := codes[position]

		switch opcode {
		case 1:
			//debug(codes, position)
			readWrite(codes, position, func(a int, b int) int {
				return a + b
			})

		case 2:
			//debug(codes, position)
			readWrite(codes, position, func(a int, b int) int {
				return a * b
			})

		case 99:
			halt = true
			break

		default:
			panic(fmt.Sprintf("Invalid opcode: %d", opcode))
		}

		position = position + 4
	}

	return codes
}

func Compute(program string) []int {
	return Reader(Parser(program))
}
