package main

import "github.com/goburrow/modbus"

func main() {
	client := modbus.TCPClient("192.168.1.32:502")
	// Read input register 9
	for true {
		client.WriteSingleRegister(1, 0)
		client.WriteSingleRegister(1, 1)
	}
}
