package solutions

import (
	"github.com/aewens/aoc19/pkg/utilities"
)

func init() {
	Map[12] = Solution12
}

type Moon struct {
	X int
	Y int
	Z int
}

type Force struct {
	X int
	Y int
	Z int
}

type System struct {
	Moons  []*Moon
	Forces []*Force
}

func gcd(a int, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

func lcm(a int, b int) int {
	result := a * b / gcd(a, b)
	return result
}

func parseCoordinates(entry string) *Moon {
	moon := &Moon{}
	entrySansBrackets := entry[1 : len(entry)-1]
	for _, coord := range Separate(entrySansBrackets, ", ") {
		pair := Separate(coord, "=")
		value := utilities.StringToInt(pair[1])
		switch pair[0] {
		case "x":
			moon.X = value
		case "y":
			moon.Y = value
		case "z":
			moon.Z = value
		}
	}

	return moon
}

func ApplyGravity(system *System) {
	for m, moon := range system.Moons {
		for mm, mMoon := range system.Moons {
			if m == mm {
				continue
			}

			if mMoon.X > moon.X {
				system.Forces[m].X = system.Forces[m].X + 1
			} else if mMoon.X < moon.X {
				system.Forces[m].X = system.Forces[m].X - 1
			}

			if mMoon.Y > moon.Y {
				system.Forces[m].Y = system.Forces[m].Y + 1
			} else if mMoon.Y < moon.Y {
				system.Forces[m].Y = system.Forces[m].Y - 1
			}

			if mMoon.Z > moon.Z {
				system.Forces[m].Z = system.Forces[m].Z + 1
			} else if mMoon.Z < moon.Z {
				system.Forces[m].Z = system.Forces[m].Z - 1
			}
		}
	}
}

func ApplyAxisGravity(system *System, axis int) {
	for m, moon := range system.Moons {
		for mm, mMoon := range system.Moons {
			if m == mm {
				continue
			}

			switch axis {
			case 0:
				if mMoon.X > moon.X {
					system.Forces[m].X = system.Forces[m].X + 1
				} else if mMoon.X < moon.X {
					system.Forces[m].X = system.Forces[m].X - 1
				}
			case 1:
				if mMoon.Y > moon.Y {
					system.Forces[m].Y = system.Forces[m].Y + 1
				} else if mMoon.Y < moon.Y {
					system.Forces[m].Y = system.Forces[m].Y - 1
				}
			case 2:
				if mMoon.Z > moon.Z {
					system.Forces[m].Z = system.Forces[m].Z + 1
				} else if mMoon.Z < moon.Z {
					system.Forces[m].Z = system.Forces[m].Z - 1
				}
			}
		}
	}
}

func ApplyVelocity(system *System) {
	for f, force := range system.Forces {
		moon := system.Moons[f]
		moon.X = moon.X + force.X
		moon.Y = moon.Y + force.Y
		moon.Z = moon.Z + force.Z
	}
}

func ApplyAxisVelocity(system *System, axis int) {
	for f, force := range system.Forces {
		moon := system.Moons[f]
		switch axis {
		case 0:
			moon.X = moon.X + force.X
		case 1:
			moon.Y = moon.Y + force.Y
		case 2:
			moon.Z = moon.Z + force.Z
		}
	}
}

func MoonStep(system *System) {
	ApplyGravity(system)
	ApplyVelocity(system)
}

func MoonAxisStep(system *System, axis int) {
	ApplyAxisGravity(system, axis)
	ApplyAxisVelocity(system, axis)
}

func CheckAxis(system *System, init *System, axis int) bool {
	valid := true
	for m, moon := range system.Moons {
		force := system.Forces[m]
		initMoon := init.Moons[m]
		initForce := init.Forces[m]

		switch axis {
		case 0:
			if moon.X != initMoon.X || force.X != initForce.X {
				valid = false
			}
		case 1:
			if moon.Y != initMoon.Y || force.Y != initForce.Y {
				valid = false
			}
		case 2:
			if moon.Z != initMoon.Z || force.Z != initForce.Z {
				valid = false
			}
		}

		if !valid {
			break
		}
	}

	return valid
}

func SearchAxis(system *System, init *System, axis int) int {
	steps := 0
	for {
		MoonAxisStep(system, axis)
		steps = steps + 1

		match := CheckAxis(system, init, axis)
		if match {
			return steps
		}
	}
}

func CalculateEnergy(system *System) int {
	energy := 0
	for m, moon := range system.Moons {
		potentialEnergy := 0
		if moon.X < 0 {
			potentialEnergy = potentialEnergy - moon.X
		} else {
			potentialEnergy = potentialEnergy + moon.X
		}

		if moon.Y < 0 {
			potentialEnergy = potentialEnergy - moon.Y
		} else {
			potentialEnergy = potentialEnergy + moon.Y
		}

		if moon.Z < 0 {
			potentialEnergy = potentialEnergy - moon.Z
		} else {
			potentialEnergy = potentialEnergy + moon.Z
		}

		kineticEnergy := 0
		force := system.Forces[m]
		if force.X < 0 {
			kineticEnergy = kineticEnergy - force.X
		} else {
			kineticEnergy = kineticEnergy + force.X
		}

		if force.Y < 0 {
			kineticEnergy = kineticEnergy - force.Y
		} else {
			kineticEnergy = kineticEnergy + force.Y
		}

		if force.Z < 0 {
			kineticEnergy = kineticEnergy - force.Z
		} else {
			kineticEnergy = kineticEnergy + force.Z
		}

		energy = energy + potentialEnergy*kineticEnergy
	}

	return energy
}

func Solution12(lines chan string) {
	moons := []*Moon{}
	forces := []*Force{}

	initMoons := []*Moon{}
	initForces := []*Force{}
	for line := range lines {
		moon := parseCoordinates(line)
		moons = append(moons, moon)
		forces = append(forces, &Force{})

		initMoon := parseCoordinates(line)
		initMoons = append(initMoons, initMoon)
		initForces = append(initForces, &Force{})
	}

	system := &System{
		Moons:  moons,
		Forces: forces,
	}

	initSystem := &System{
		Moons:  initMoons,
		Forces: initForces,
	}

	for s := 0; s < 1000; s++ {
		MoonStep(system)
	}
	energy := CalculateEnergy(system)
	Display(1, energy)

	cycles := []int{}
	for a := 0; a < 3; a++ {
		steps := SearchAxis(system, initSystem, a)
		cycles = append(cycles, steps+1000)
	}

	Display(2, lcm(cycles[0], lcm(cycles[1], cycles[2])))
}
