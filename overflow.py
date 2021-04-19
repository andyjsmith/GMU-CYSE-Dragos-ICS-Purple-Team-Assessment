from pyModbusTCP.client import ModbusClient
import time
import paramiko


def exec_ssh_cmds(cmds, out=True):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.1.2", port=22, username="admin",
                   password="")
    # stdin, stdout, stderr = client.exec_command("")
    # print(stdout.read().decode("utf-8"))
    cmd = "\n".join(cmds)
    stdin, stdout, stderr = client.exec_command(cmd)
    stdout.read()  # must read output of command or it doesn't run *facepalm*
    client.close()


SERVER_HOST = "192.168.1.20"
SERVER_PORT = 502
SERVER_U_ID = 1

c = ModbusClient()
c2 = ModbusClient()

# uncomment this line to see debug message
# c.debug(True)

# define modbus server host, port and unit_id
c.host(SERVER_HOST)
c.port(SERVER_PORT)
c.unit_id(SERVER_U_ID)

c2.host("192.168.1.30")
c2.port(502)
c2.unit_id(1)
c2.open()
c2.close()

cmds = [
    "config switch physical-port",
    "edit port4",
    "set status down",
    "end"
]
exec_ssh_cmds(cmds)

# open or reconnect TCP to server
if not c.is_open():
    if not c.open():
        print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

if c.is_open():
    while True:
        # Turn pump on
        c.write_single_coil(1, True)
        # Set pump to 100%
        c.write_single_register(3, 0x64)
        val = c.read_coils(5)[0]
        print(val)

        c2.write_single_coil(1, True)

        if val:
            c.write_single_coil(1, False)

        time.sleep(0.2)
