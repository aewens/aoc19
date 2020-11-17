package solutions

import (
	"github.com/aewens/aoc19/pkg/intcode"
)

/**
 * NOTE: Currently has a bug where it will sometime fail with:
 *  panic: Unknown mode: 10 | X
 *
 * Where X is the current position of the intcode computer. This is from a race
 * condition that I am in no mood to fix right now. Just run it again and it
 * should fix the issue.
 *
 * A potential fix for this would be not using channels and just passing in I/O
 * using a queue or int arrays.
 */

func init() {
	Map[11] = Solution11
}

type Ship struct {
	MinX   int
	MinY   int
	MaxX   int
	MaxY   int
	Panels map[int]map[int]int
	Paint  map[int]map[int]bool
}

type Robot struct {
	Input     chan int
	Output    chan int
	Computer  *intcode.Computer
	Direction int
	X         int
	Y         int
}

func (robot *Robot) Step(ship *Ship) bool {
	action := robot.Computer.StepUntil(3, 4, 99)
	switch action {
	case 3:
		_, ok := ship.Panels[robot.Y]
		if !ok {
			ship.Panels[robot.Y] = make(map[int]int)
		}
		panel, ok := ship.Panels[robot.Y][robot.X]
		if !ok {
			ship.Panels[robot.Y][robot.X] = 0
			panel = 0
		}
		go robot.Computer.Input(panel)
		robot.Computer.Step()
	case 4:
		go robot.Computer.Step()
		paint := robot.Computer.Output()
		ship.Panels[robot.Y][robot.X] = paint
		_, ok := ship.Paint[robot.Y]
		if !ok {
			ship.Paint[robot.Y] = make(map[int]bool)
		}
		ship.Paint[robot.Y][robot.X] = true

		action := robot.Computer.StepUntil(4, 99)
		if action == 99 {
			return true
		}

		go robot.Computer.Step()
		direction := robot.Computer.Output()
		//Display(-31, direction)
		switch direction {
		case 0:
			robot.Direction = (robot.Direction - 1) % 4
			if robot.Direction < 0 {
				robot.Direction = robot.Direction + 4
			}
		case 1:
			robot.Direction = (robot.Direction + 1) % 4
		default:
			panic("Invalid direction")
		}

		switch robot.Direction {
		case 0:
			robot.Y = robot.Y - 1
			if robot.Y > ship.MaxY {
				ship.MaxY = robot.Y
			}
		case 1:
			robot.X = robot.X + 1
			if robot.X > ship.MaxX {
				ship.MaxX = robot.X
			}
		case 2:
			robot.Y = robot.Y + 1
			if robot.Y < ship.MinY {
				ship.MinY = robot.Y
			}
		case 3:
			robot.X = robot.X - 1
			if robot.X < ship.MinX {
				ship.MinX = robot.X
			}
		default:
			panic("Invalid robot direction")
		}
	case 99:
		return true
	}

	return false
}

func (robot *Robot) Display(ship *Ship) {
	Clear()

	for y := ship.MinY; y < ship.MaxY; y++ {
		row := ""
		for x := ship.MinX; x < ship.MaxX; x++ {
			panel := ship.Panels[y][x]
			if panel == 1 {
				row = row + "@"
			} else {
				row = row + " "
			}
		}
		Display(0, row)
	}
}

func (robot *Robot) Run(ship *Ship) int {
	done := make(chan bool)

	go func() {
		for {
			halted := robot.Step(ship)
			if halted {
				done <- true
				break
			}
		}
	}()

	<-done
	panels := 0
	for _, row := range ship.Paint {
		panels = panels + len(row)
	}
	//robot.Display(ship)

	return panels
}

func Solution11(lines chan string) {
	program := <-lines
	computer := intcode.BufferedNew(program)
	ship := &Ship{
		MinX:   0,
		MinY:   0,
		MaxX:   0,
		MaxY:   0,
		Panels: make(map[int]map[int]int),
		Paint:  make(map[int]map[int]bool),
	}
	robot := &Robot{
		Input:     make(chan int),
		Output:    make(chan int),
		Computer:  computer,
		Direction: 0,
		X:         0,
		Y:         0,
	}

	panels := robot.Run(ship)
	Display(1, panels)
}
