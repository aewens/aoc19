package solutions

import (
	"github.com/aewens/aoc19/pkg/intcode"
)

func init() {
	Map[7] = Solution7
}

func permutations(xs []int, i int, all [][]int) [][]int {
	if i == 1 {
		tmp := make([]int, len(xs))
		copy(tmp, xs)
		all = append(all, tmp)
	} else {
		for j := 0; j < i; j++ {
			all = permutations(xs, i-1, all)
			if i%2 == 1 {
				tmp := xs[j]
				xs[j] = xs[i-1]
				xs[i-1] = tmp
			} else {
				tmp := xs[0]
				xs[0] = xs[i-1]
				xs[i-1] = tmp
			}
		}
	}
	return all
}

func Permutate(xs []int) [][]int {
	return permutations(xs, len(xs), [][]int{})
}

func CreateNetwork(program string, amount int) []*intcode.Computer {
	computers := []*intcode.Computer{}

	for a := 0; a < amount; a++ {
		computer := intcode.BufferedNew(program)
		computers = append(computers, computer)
	}

	return computers
}

func ThrusterSignal(computers []*intcode.Computer, phases []int) int {
	go func() {
		for p := range phases {
			computers[p].Input(phases[p])
		}

		computers[0].Input(0)
		for c := 0; c < len(computers)-1; c++ {
			computers[c+1].Input(computers[c].Output())
		}
	}()

	for _, computer := range computers {
		go computer.RunAndReset()
	}

	output := computers[len(computers)-1].Output()

	return output
}

func Solution7(lines chan string) {
	//<-lines
	//program := "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"

	program := <-lines
	computers := CreateNetwork(program, 5)

	maxSignal := 0
	for _, phases := range Permutate([]int{0, 1, 2, 3, 4}) {
		signal := ThrusterSignal(computers, phases)
		if signal > maxSignal {
			maxSignal = signal
		}
	}

	Display(1, maxSignal)
}
