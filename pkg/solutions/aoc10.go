package solutions

import (
	"math"
)

func init() {
	Map[10] = Solution10
}

type AsteroidMap struct {
	Map       [][]string
	Asteroids [][]int
}

func BuildAsteroidMap(lines chan string) *AsteroidMap {
	y := 0
	aMap := [][]string{}
	asteroids := [][]int{}
	for line := range lines {
		row := []string{}
		for x, block := range Separate(line, "") {
			row = append(row, block)
			if block == "#" {
				asteroids = append(asteroids, []int{y, x})
			}
		}
		y = y + 1
		aMap = append(aMap, row)
	}

	return &AsteroidMap{
		Map:       aMap,
		Asteroids: asteroids,
	}
}

func MostVisibleAsteroids(asteroidMap *AsteroidMap) int {
	mostVisible := 0
	for a, asteroid := range asteroidMap.Asteroids {
		y := asteroid[0]
		x := asteroid[1]

		visible := make(map[float64]bool)
		for aa, aAsteroid := range asteroidMap.Asteroids {
			if a == aa {
				continue
			}

			ay := aAsteroid[0]
			ax := aAsteroid[1]
			dy := float64(y - ay)
			dx := float64(x - ax)
			angle := math.Atan2(dy, dx)
			
			_, ok := visible[angle]
			if !ok {
				visible[angle] = true
			}
		}

		if len(visible) > mostVisible {
			mostVisible = len(visible)
		}
	}

	return mostVisible
}

func Solution10(lines chan string) {
	asteroidMap := BuildAsteroidMap(lines)
	visible := MostVisibleAsteroids(asteroidMap)
	Display(1, visible)
}
