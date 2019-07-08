package server

import (
	"log"
	"net/http"
)

var logTag = "server: "

// Start http and websockets server
func Start() {
	InitConfig()

	log.Println("Starting server...")

	/*
		Callbacks do admin
	*/

	http.Handle("/", http.FileServer(http.Dir("static")))

	/*
		Start Server
	*/

	log.Println("Listening on port " + cfg.ServerPort)

	http.ListenAndServe(":"+cfg.ServerPort, nil)
}
