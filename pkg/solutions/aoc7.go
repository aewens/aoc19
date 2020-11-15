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

func LoopingThrusterSignal(computers []*intcode.Computer, phases []int) int {
	result := make(chan int)

	go func() {
		for p := range phases {
			action := computers[p].StepUntil(3, 99)
			if action == 99 {
				continue
			}
			go computers[p].Input(phases[p])
			computers[p].Step()
		}

		go computers[0].Input(0)
		computers[0].StepUntil(4, 99)
		for {

			for c := 0; c < len(computers)-1; c++ {
				action := computers[c].StepUntil(4, 99)
				if action == 99 {
					continue
				}

				go computers[c].Step()
				output := computers[c].Output()

				go computers[c+1].Input(output)
				computers[c+1].StepUntil(4, 99)
			}

			computer := computers[len(computers)-1]

			action := computer.StepUntil(4, 99)
			if action == 99 {
				result <- -1
				break
			}

			next := computers[0].StepUntil(3, 4, 99)

			go computer.Step()
			output := computer.Output()

			if next == 3 {
				go computers[0].Input(output)
				computers[0].StepUntil(4, 99)
				continue
			}

			result <- output
			break
		}
	}()

	signal := <-result
	for _, computer := range computers {
		computer.Reset()
	}

	return signal
}

func Solution7(lines chan string) {
	//<-lines
	//program := "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"

	program := <-lines
	computers := CreateNetwork(program, 5)

	maxSignals := []int{0, 0}
	for _, phases := range Permutate([]int{0, 1, 2, 3, 4}) {
		signal := ThrusterSignal(computers, phases)
		if signal > maxSignals[0] {
			maxSignals[0] = signal
		}
	}

	Display(1, maxSignals[0])

	for _, phases := range Permutate([]int{5, 6, 7, 8, 9}) {
		signal := LoopingThrusterSignal(computers, phases)
		if signal > maxSignals[1] {
			maxSignals[1] = signal
		}
	}

	Display(2, maxSignals[1])
}
