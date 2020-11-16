package solutions

import (
	"math"
	"sort"
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

func MostVisibleAsteroids(asteroidMap *AsteroidMap) (int, int) {
	mostVisible := 0
	bestAsteroid := -1
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
			bestAsteroid = a
		}
	}

	return mostVisible, bestAsteroid
}

func SpinLaserUntil(asteroidMap *AsteroidMap, index int, stop int) []int {
	angles := make(map[float64][]int)
	proximity := make(map[int]float64)

	station := asteroidMap.Asteroids[index]
	sy := float64(station[0])
	sx := float64(station[1])

	for a, asteroid := range asteroidMap.Asteroids {
		if a == index {
			continue
		}
		y := float64(asteroid[0])
		x := float64(asteroid[1])
		dy := sy - y
		dx := sx - x
		angle := math.Atan2(dy, dx)
		distance := math.Sqrt(math.Pow(dx, 2) + math.Pow(dy, 2))

		_, ok := angles[angle]
		if !ok {
			angles[angle] = []int{}
		}

		angles[angle] = append(angles[angle], a)
		proximity[a] = distance
	}

	// Start laser pointing up
	laserAngle := math.Atan2(1, 0)

	angleKeys := []float64{}
	for angleKey := range angles {
		angleKeys = append(angleKeys, angleKey)
	}

	// Find first index where laser will hit
	firstIndex := -1
	sort.Float64s(angleKeys)
	for ak, angleKey := range angleKeys {
		if angleKey >= laserAngle {
			firstIndex = ak
			break
		}
	}

	count := 0
	vaporized := make(map[int]bool)
	rotations := len(angleKeys)
	for {
		for i := 0; i < rotations; i++ {
			angleIndex := (firstIndex + i) % rotations
			asteroids := angles[angleKeys[angleIndex]]

			closestAsteroid := -1
			var closest float64 = -1
			for _, asteroid := range asteroids {
				_, ok := vaporized[asteroid]
				if ok {
					continue
				}

				distance := proximity[asteroid]
				if closest == -1 || distance < closest {
					closest = distance
					closestAsteroid = asteroid
				}
			}

			if closest == -1 {
				continue
			}

			if count+1 == stop {
				return asteroidMap.Asteroids[closestAsteroid]
			}

			vaporized[closestAsteroid] = true
			count = count + 1
		}
	}

}

func Solution10(lines chan string) {
	asteroidMap := BuildAsteroidMap(lines)
	visible, station := MostVisibleAsteroids(asteroidMap)
	Display(1, visible)

	asteroid := SpinLaserUntil(asteroidMap, station, 200)
	Display(2, asteroid[1]*100+asteroid[0])
}
