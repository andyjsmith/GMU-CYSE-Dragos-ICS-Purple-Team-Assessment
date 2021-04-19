from pyModbusTCP.client import ModbusClient
import time

SERVER_HOST = "192.168.1.32"
SERVER_PORT = 502
SERVER_U_ID = 1

c = ModbusClient()

# uncomment this line to see debug message
c.debug(True)

# define modbus server host, port and unit_id
c.host(SERVER_HOST)
c.port(SERVER_PORT)
c.unit_id(SERVER_U_ID)


while True:
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    if c.is_open():
        #print("write bits")
        addr = 1
        #print(f"Addr {addr}")
        speed = 0.0
        c.write_single_register(addr, 1)  # Red
        time.sleep(speed)
        c.write_single_register(addr, 0)  # Blue
        time.sleep(speed)
