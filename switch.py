import sys
import os
import time
import argparse
import paramiko
from colorama import Fore, Style, init

init()

parser = argparse.ArgumentParser(
    description="Control switch port configuration")
parser.add_argument('--up', action='store_true')
parser.add_argument('--down', action='store_true')
args = parser.parse_args()


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


ports = [1, 2, 3, 4]

if args.down:
    action = "down"
else:
    action = "up"

# Set PLC port to DOWN
cmds = []
for port in ports:
    cmds += [
        "config switch physical-port",
        f"edit port{port}",
        f"set status {action}",
        "end"
    ]
print(f"Setting switch port(s) {ports} to {action}: ", end="", flush=True)
exec_ssh_cmds(cmds)
print(f"[{Fore.GREEN}DONE{Style.RESET_ALL}]")
