from pyModbusTCP.client import ModbusClient
import time

SERVER_HOST = "192.168.1.20"
SERVER_PORT = 502
SERVER_U_ID = 1

c = ModbusClient()

# uncomment this line to see debug message
# c.debug(True)

# define modbus server host, port and unit_id
c.host(SERVER_HOST)
c.port(SERVER_PORT)
c.unit_id(SERVER_U_ID)

speed = 0.001

while True:
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    # if open() is ok, write coils
    if c.is_open():
        addr = 2  # addr = reference number in wireshark
        is_ok = c.write_single_coil(addr, True)  # Solenoid on
        time.sleep(speed)
        is_ok = c.write_single_coil(addr, False)  # Solenoid off

        time.sleep(speed)
