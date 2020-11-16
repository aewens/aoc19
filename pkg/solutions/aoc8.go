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
	for layer := 0; layer < layerCount; layer++ {
		layerPosition := layer * layerSize
		layerData := imageData[layerPosition:layerPosition+layerSize]

		zeros := 0
		ones := 0
		twos := 0
		for _, rawDigit := range Separate(layerData, "") {
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
		}

		if fewestZeros == -1 || zeros < fewestZeros {
			fewestZeros = zeros
			fewestZeroCode = ones * twos
		}
	}

	Display(1, fewestZeroCode)
}
