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
	Ball     *Tile
	Paddle   *Tile
	Width    int
	Height   int
	Score    int
	Auto     bool
}

func (arcade *Arcade) Display() {
	Clear()
	Display(10, arcade.Score)
	for y := 0; y < arcade.Height; y++ {
		row := ""
		for x := 0; x < arcade.Width; x++ {
			row = row + arcade.Monitor[y][x]
		}

		Display(20, row)
	}
}

func (arcade *Arcade) Reset() {
	arcade.Computer.Reset()
	arcade.Monitor = make(map[int]map[int]string)
	arcade.Tiles = []*Tile{}
	arcade.Width = 0
	arcade.Height = 0
	arcade.Score = 0
}

func (arcade *Arcade) Run(display bool) {
	arcade.Tiles = []*Tile{}
	for {
		action := arcade.Computer.StepUntil(3, 4, 99)
		if action == 3 || action == 99 {
			if action == 3 && display {
				if arcade.Auto {
					if arcade.Ball.X < arcade.Paddle.X {
						arcade.Computer.Input(-1)
					} else if arcade.Ball.X > arcade.Paddle.X {
						arcade.Computer.Input(1)
					} else {
						arcade.Computer.Input(0)
					}
				} else {
					arcade.Display()
					joystick := Input("(a/s/d)> ")
					switch joystick {
					case "a":
						arcade.Computer.Input(-1)
					case "s":
						arcade.Computer.Input(0)
					case "d":
						arcade.Computer.Input(1)
					default:
						panic("Invalid joystick action")
					}
				}
				arcade.Computer.Step()
				continue
			}
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

		if tile.X == -1 && tile.Y == 0 {
			arcade.Score = tile.ID
			continue
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
			arcade.Paddle = tile
		case 4:
			arcade.Monitor[tile.Y][tile.X] = "@"
			arcade.Ball = tile
		}
	}
}

func (arcade *Arcade) InsertQuarters() {
	arcade.Computer.Memory[0] = 2
}

func Solution13(lines chan string) {
	program := <-lines
	computer := intcode.QueuedNew(program)

	arcade := &Arcade{
		Computer: computer,
		Monitor:  make(map[int]map[int]string),
		Auto:     true,
	}

	arcade.Run(false)

	blocks := 0
	for _, tile := range arcade.Tiles {
		if tile.ID == 2 {
			blocks = blocks + 1
		}
	}
	Display(1, blocks)

	arcade.Reset()
	arcade.InsertQuarters()
	arcade.Run(true)
	Display(2, arcade.Score)

	for {
		Display(99, "Play?")
		play := Input("(y/n)> ")
		exit := false
		switch play {
		case "y":
			arcade.Auto = false
			arcade.Reset()
			arcade.InsertQuarters()
			arcade.Run(true)
		case "n":
			exit = true
			arcade.Reset()
		}

		if exit {
			break
		}
	}
}
