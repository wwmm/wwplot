package main

import (
	"log"
	"wwmm/wwplot/server"
)

var logTag = "main: "

func main() {
	// to change the flags on the default logger
	log.SetFlags(log.LstdFlags | log.Lshortfile)

	server.Start()
}
