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


cmds = [
    "config switch physical-port",
    "edit port4",
    "set status up",
    "end"
]
exec_ssh_cmds(cmds)
