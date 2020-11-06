package solutions

func init() {
	Map[1] = Solution1
}

func Solution1(lines chan string) {
	fuel := 0
	for line := range lines {
		mass := StringToInt(line)
		fuel = fuel + ((mass / 3) - 2)

		if lines == nil {
			break
		}
	}
	Display(1, IntToString(fuel))
}
