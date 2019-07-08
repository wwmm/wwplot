package server

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"os"
)

//Config é uma estrutura com algumas configurações como nome e e-mail
type Config struct {
	ServerPort string
}

var cfg Config

//InitConfig inicializa a estrutura com as configurações
func InitConfig() {
	cfg = Config{ServerPort: "40000"}

	if _, err := os.Stat("config.json"); err != nil {
		if os.IsNotExist(err) {
			// file does not exist
			log.Println(logTag +
				"Config does not exists. Creating it with default values")

			saveConfig()
		} else {
			if err != nil {
				log.Println(logTag + err.Error())
			}
		}
	} else {
		log.Println("Reading configuration...")

		f, err := ioutil.ReadFile("config.json")

		if err != nil {
			log.Fatal(logTag + err.Error())
		}

		err = json.Unmarshal([]byte(f), &cfg)

		if err != nil {
			log.Fatal(logTag + err.Error())
		}
	}
}

func saveConfig() {
	f, err := json.MarshalIndent(cfg, "", "    ")

	if err != nil {
		log.Fatal(logTag + err.Error())
	}

	err = ioutil.WriteFile("config.json", f, 0755)

	if err != nil {
		log.Fatal(logTag + err.Error())
	}
}
