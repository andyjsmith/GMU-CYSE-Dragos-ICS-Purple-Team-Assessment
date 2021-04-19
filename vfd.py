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

speed = 0.1

while True:
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    # if open() is ok, write coils
    if c.is_open():
        is_ok = c.write_single_coil(1, True)  # Solenoid on
        c.write_single_register(3, 0x64)
        # time.sleep(speed)
        # is_ok = c.write_single_coil(1, False)  # Solenoid off
        #c.write_single_register(3, 0x0)

        time.sleep(speed)
