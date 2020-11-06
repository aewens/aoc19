package utilities

import (
	"os"
	"log"
	"syscall"
	"os/signal"
)

func Cleanup() {
	r := recover()
	if r != nil {
		log.Println("[!] ", r)
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
