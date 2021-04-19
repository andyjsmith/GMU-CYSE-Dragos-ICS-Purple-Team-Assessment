import time
import argparse
from pyModbusTCP.client import ModbusClient

parser = argparse.ArgumentParser(
    description="Control power to modbus components")
parser.add_argument('--on', action='store_true')
parser.add_argument('--off', action='store_true')
args = parser.parse_args()

SERVER_HOST = "192.168.1.30"
SERVER_PORT = 502
SERVER_U_ID = 1

c = ModbusClient()

# uncomment this line to see debug message
# c.debug(True)

# define modbus server host, port and unit_id
c.host(SERVER_HOST)
c.port(SERVER_PORT)
c.unit_id(SERVER_U_ID)

# open or reconnect TCP to server
if not c.is_open():
    if not c.open():
        print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

# if open() is ok, write coils
if c.is_open():
    for addr in [0, 1, 2, 3]:
        if args.on:
            is_ok = c.write_single_coil(addr, True)  # Solenoid on
        elif args.off:
            is_ok = c.write_single_coil(addr, False)  # Solenoid on
        else:
            print("No command given")
            break
        # time.sleep(1)
        # is_ok = c.write_single_coil(addr, False)  # Solenoid off
