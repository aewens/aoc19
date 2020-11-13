package utilities

import (
	"log"
	"os"
	"os/signal"
	"strconv"
	"syscall"
)

func Cleanup() {
	r := recover()
	if r != nil {
		log.Println("[!]", r)
		os.Exit(1)
	}
	os.Exit(0)
}

func HandleSigterm() {
	sigterm := make(chan os.Signal)
	signal.Notify(sigterm, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-sigterm
		Cleanup()
	}()
}

func StringToInt(convert string) int {
	value, err := strconv.Atoi(convert)
	if err != nil {
		panic(err)
	}

	return value
}

func RuneToInt(convert rune) int {
	return int(convert - '0')
}

func IntToString(convert int) string {
	value := strconv.Itoa(convert)
	return value
}
