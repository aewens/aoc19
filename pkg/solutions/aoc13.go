package solutions

import (
	"github.com/aewens/aoc19/pkg/intcode"
)

func init() {
	Map[13] = Solution13
}

type Tile struct {
	ID int
	X  int
	Y  int
}

type Arcade struct {
	Computer *intcode.Computer
	Monitor  map[int]map[int]string
	Tiles    []*Tile
	Width    int
	Height   int
}

func (arcade *Arcade) Display() {
	Clear()
	for y := 0; y < arcade.Height; y++ {
		row := ""
		for x := 0; y < arcade.Width; x++ {
			row = row + arcade.Monitor[y][x]
		}

		Display(0, row)
	}
}

func (arcade *Arcade) Run() {
	arcade.Tiles = []*Tile{}
	for {
		action := arcade.Computer.StepUntil(3, 4, 99)
		if action == 3 || action == 99 {
			break
		}

		tile := &Tile{}
		halted := false
		for i := 0; i < 3; i++ {
			action := arcade.Computer.StepUntil(4, 99)
			if action == 99 {
				halted = true
			}
			arcade.Computer.Step()

			output := arcade.Computer.Output()
			switch i {
			case 0:
				tile.X = output
				if tile.X > arcade.Width {
					arcade.Width = tile.X
				}
			case 1:
				tile.Y = output
				if tile.Y > arcade.Height {
					arcade.Height = tile.Y
				}
			case 2:
				tile.ID = output
			}
		}

		if halted {
			break
		}

		arcade.Tiles = append(arcade.Tiles, tile)

		_, ok := arcade.Monitor[tile.Y]
		if !ok {
			arcade.Monitor[tile.Y] = make(map[int]string)
		}
		switch tile.ID {
		case 0:
			arcade.Monitor[tile.Y][tile.X] = " "
		case 1:
			arcade.Monitor[tile.Y][tile.X] = "|"
		case 2:
			arcade.Monitor[tile.Y][tile.X] = "#"
		case 3:
			arcade.Monitor[tile.Y][tile.X] = "-"
		case 4:
			arcade.Monitor[tile.Y][tile.X] = "@"
		}
	}
}

func Solution13(lines chan string) {
	program := <-lines
	computer := intcode.QueuedNew(program)

	arcade := &Arcade{
		Computer: computer,
		Monitor:  make(map[int]map[int]string),
	}

	arcade.Run()

	blocks := 0
	for _, tile := range arcade.Tiles {
		if tile.ID == 2 {
			blocks = blocks + 1
		}
	}
	Display(1, blocks)
}
