package solutions

import (
	"os"
	"fmt"
	"bufio"
	"strconv"
)

type Solutions map[int]func(chan string)
var Map Solutions = make(Solutions)

func ReadLines(path string, lines chan string) {
	file, err := os.Open(path)
	if err != nil {
		panic(err)
	}

	defer file.Close()
	scanner := bufio.NewScanner(file)
	
	for scanner.Scan() {
		line := scanner.Text()
		lines <-line
	}

	close(lines)

	err = scanner.Err()
	if err != nil {
		panic(err)
	}
}

func Display(answer int, text interface{}) {
	fmt.Printf("[%d] %#v\n", answer, text)
}

func StringToInt(convert string) int {
	value, err := strconv.Atoi(convert)
	if err != nil {
		panic(err)
	}

	return value
}

func IntToString(convert int) string {
	value := strconv.Itoa(convert)
	return value
}
