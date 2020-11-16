package solutions

import (
	"github.com/aewens/aoc19/pkg/utilities"
)

func init() {
	Map[8] = Solution8
}

func Solution8(lines chan string) {
	imageData := <-lines

	width := 25
	height := 6
	layerSize := width * height
	layerCount := len(imageData) / layerSize

	fewestZeros := -1
	fewestZeroCode := -1

	finalImageData := [][]int{}
	for h := 0; h < height; h++ {
		row := []int{}
		for w := 0; w < width; w++ {
			row = append(row, -1)
		}
		finalImageData = append(finalImageData, row)
	}

	for layer := 0; layer < layerCount; layer++ {
		layerPosition := layer * layerSize
		layerData := imageData[layerPosition : layerPosition+layerSize]

		zeros := 0
		ones := 0
		twos := 0
		for r, rawDigit := range Separate(layerData, "") {
			digit := utilities.StringToInt(rawDigit)

			switch digit {
			case 0:
				zeros = zeros + 1
			case 1:
				ones = ones + 1
			case 2:
				twos = twos + 1
			default:
				panic("Invalid digit")
			}

			x := r % width
			y := r / width
			pixel := finalImageData[y][x]
			if pixel == -1 || pixel == 2 {
				finalImageData[y][x] = digit
			}
		}

		if fewestZeros == -1 || zeros < fewestZeros {
			fewestZeros = zeros
			fewestZeroCode = ones * twos
		}
	}

	Display(1, fewestZeroCode)
	for h := 0; h < height; h++ {
		row := ""
		for w := 0; w < width; w++ {
			pixel := finalImageData[h][w]
			if pixel == 0 {
				row = row + " "
			} else {
				row = row + "@"
			}
		}

		Display(2, row)
	}
}
