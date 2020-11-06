package solutions

import (
	"os"
	"fmt"
	"bufio"
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
		lines <-scanner.Text()
	}

	close(lines)

	err = scanner.Err()
	if err != nil {
		panic(err)
	}
}

func Display(answer int, text string) {
	fmt.Printf("[%d] %s\n", answer, text)
}
