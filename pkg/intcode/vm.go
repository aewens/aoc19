package intcode

import (
	"fmt"
	"strings"

	"github.com/aewens/aoc19/pkg/utilities"
)

type Computer struct {
	Position  int
	Codes     []int
	Memory    []int
}

type Opcode struct {
	Value int
	Modes []int
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
		code := utilities.StringToInt(instruction)
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

func (computer *Computer) CheckAddress(address int) {
	if address < 0 || address >= len(computer.Memory) {
		panic(fmt.Sprintf("Address %d is out of bounds", address))
	}
}

func (computer *Computer) ReadMemory(address int) int {
	computer.CheckAddress(address)
	return computer.Memory[address]
}

func (computer *Computer) WriteMemory(address int, value int) {
	computer.CheckAddress(address)
	computer.Memory[address] = value
}

func (computer *Computer) Next() {
	computer.Position = computer.Position + 1
}

func (computer *Computer) Read() int {
	return computer.ReadMemory(computer.Position)
}

func (computer *Computer) ReadNext() int {
	computer.Next()
	return computer.Read()
}

func (computer *Computer) ReadFromNext() int {
	return computer.ReadMemory(computer.ReadNext())
}

func (computer *Computer) ReadNextGivenMode(mode int) int {
	switch mode {
	case 0:
		return computer.ReadFromNext()

	case 1:
		return computer.ReadNext()

	default:
		panic(fmt.Sprintf("Unknown mode: %d", mode))
	}
}

func (computer *Computer) WriteToNext(value int) {
	computer.WriteMemory(computer.ReadNext(), value)
}

func (computer *Computer) WriteNextGivenMode(mode int, value int) {
	switch mode {
	case 0:
		computer.WriteToNext(value)

	case 1:
		panic("Illegal mode for write operations")

	default:
		panic(fmt.Sprintf("Unknown mode: %d", mode))
	}
}

func (computer *Computer) ReadOpcode() *Opcode {
	modes := []int{}
	value := computer.Read()
	if value == 99 {
		return &Opcode{value, modes}
	}

	parsed := utilities.IntToString(value)
	parsedSize := len(parsed)
	if parsedSize < 2 {
		parsed = "0" + parsed
		parsedSize = 2
	}

	opcode := utilities.StringToInt(parsed[parsedSize-2:])

	params := parsed[:parsedSize-2]
	paramsSize := len(params)

	expectedModes := make(map[int]int)
	expectedModes[1] = 3
	expectedModes[2] = 3
	expectedModes[3] = 1
	expectedModes[4] = 1

	expecting, ok := expectedModes[opcode]
	if !ok {
		panic(fmt.Sprintf("Unknown mode: %d", opcode))
	}

	// Left-pad the missing zeroes
	if paramsSize < expecting {
		for e := 0; e < expecting - paramsSize; e++ {
			params = "0" + params
		}
		paramsSize = expecting
	}

	for p := 1; p <= paramsSize; p++  {
		param := rune(params[paramsSize-p])
		mode := utilities.RuneToInt(param)
		modes = append(modes, mode)
	}

	return &Opcode{opcode, modes}
}


func (computer *Computer) Run() []int {
	halt := false

	for {
		opcode := computer.ReadOpcode()

		switch opcode.Value {
		case 1:
			value1 := computer.ReadNextGivenMode(opcode.Modes[0])
			value2 := computer.ReadNextGivenMode(opcode.Modes[1])
			computer.WriteNextGivenMode(opcode.Modes[2], value1 + value2)

		case 2:
			value1 := computer.ReadNextGivenMode(opcode.Modes[0])
			value2 := computer.ReadNextGivenMode(opcode.Modes[1])
			computer.WriteNextGivenMode(opcode.Modes[2], value1 * value2)

		case 3:
			var input int
			_, err := fmt.Scan(&input)
			if err != nil {
				panic(err)
			}

			computer.WriteNextGivenMode(opcode.Modes[0], input)

		case 4:
			value := computer.ReadNextGivenMode(opcode.Modes[0])
			fmt.Printf("%d\n", value)

		case 99:
			halt = true

		default:
			panic(fmt.Sprintf("Invalid opcode: %d", opcode))
		}

		if halt {
			break
		}

		computer.Next()
	}

	return computer.Memory
}

func (computer *Computer) Reset() {
	computer.Position = 0
	computer.Memory = save(computer.Codes)
}

func (computer *Computer) Load(program string) {
	computer.Codes = Parser(program)
	computer.Reset()
}
