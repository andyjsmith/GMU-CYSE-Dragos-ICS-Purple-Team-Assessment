from subprocess import check_output, Popen, PIPE
import sys
import os
import time
import netifaces
import ipaddress
import signal
import paramiko
from colorama import Fore, Style, init
from pyModbusTCP.server import ModbusServer, DataBank

init()

# TODO give option to choose from list of interface names
interface = "Ethernet 3"
targetaddr = "192.168.1.20"
targetsubnet = "255.255.255.0"
targetgateway = "192.168.1.1"


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
    # print(stdout.read().decode("utf-8"))
    # for cmd in cmds:
    #     stdin, stdout, stderr = client.exec_command(cmd)
    #     if out:
    #         print(cmd)
    #         print(stdout.read().decode("utf-8"))


def getip():
    addr = None
    subnet = None
    gateway = None
    if os.name == 'nt':
        # Windows
        rawip = str(check_output(["netsh", "interface", "ipv4",
                                  "show", "addresses", interface])).split("\\r\\n")
        for i in rawip:
            if "IP Address" in i:
                addr = i.strip().split(" ")[-1].strip()
            if "Subnet Prefix" in i:
                subnet = i.strip().split(" ")[-1].split(")")[0].strip()
            if "Default Gateway" in i:
                gateway = i.strip().split(" ")[-1].strip()
    else:
        # Linux
        net = netifaces.ifaddresses(interface)[netifaces.AF_INET]
        addr = net[0]["addr"]
        subnet = net[0]["netmask"]
    return addr, subnet, gateway


def set_ip(interface, addr, subnet, gateway):
    if os.name == 'nt':
        # Windows
        setip = check_output(["netsh", "interface", "ipv4", "set", "address",
                              f'{interface}', "static", targetaddr, targetsubnet, targetgateway])
    else:
        # Linux:
        # sudo ip addr del local 172.20.56.227/20 dev eth0
        cidr = ipaddress.IPv4Network('0.0.0.0/' + subnet).prefixlen
        delip = check_output(["ip", "addr", "del", "local",
                              f"{addr}/{cidr}", "dev", interface])
        # sudo ip addr add 172.20.56.226/20 broadcast 172.20.63.255 dev eth0
        cidr = ipaddress.IPv4Network('0.0.0.0/' + targetsubnet).prefixlen
        broadcast = ipaddress.ip_network(
            f"{targetaddr}/{cidr}", strict=False).broadcast_address
        setip = check_output(["ip", "addr", "add", "local",
                              f"{targetaddr}/{cidr}", "broadcast", broadcast, "dev", interface])


def reset_ip(interface, addr, subnet, gateway):
    if os.name == 'nt':
        # Change back to original static IP just in case
        setip = check_output(["netsh", "interface", "ipv4", "set", "address",
                              f'{interface}', "static", addr, subnet, gateway])
        # Set to DHCP
        # setip = check_output(["netsh", "interface", "ipv4", "set", "address",
        #                       f'{interface}', "dhcp"])
    else:
        pass

# Get current IP so it can be reset later


def getip_check():
    addr, subnet, gateway = getip()
    if addr is None:
        print(f"[{Fore.RED}FAIL{Style.RESET_ALL}]")
        sys.exit()
    if "169.254" in addr:
        print(f"[{Fore.RED}FAIL{Style.RESET_ALL}]")
        print(f"{Fore.RED}IP address is IPv6 autoconfiguration{Style.RESET_ALL}")
        sys.exit()
    print(f"[{Fore.GREEN}DONE{Style.RESET_ALL}]")
    return addr, subnet, gateway


################
# BEGIN SCRIPT #
################


print("Getting starting IP: ", end="", flush=True)
addr, subnet, gateway = getip_check()
print(f"Starting IP: {addr} {subnet} {gateway}")


# Register Ctrl+C signal handler
def signal_handler(sig, frame):
    print(f"{Fore.YELLOW}Received interrupt, cleaning up and exiting{Style.RESET_ALL}")
    # Reset IP back to original
    print("Resetting local IP: ", end="", flush=True)
    reset_ip(interface, addr, subnet, gateway)
    time.sleep(5)
    print(f"[{Fore.GREEN}DONE{Style.RESET_ALL}]")

    # Set PLC port to UP
    print("Setting PLC port to UP: ", end="", flush=True)
    cmds = [
        "config switch physical-port",
        "edit port3",
        "set status up",
        "end"
    ]
    exec_ssh_cmds(cmds)
    print(f"[{Fore.GREEN}DONE{Style.RESET_ALL}]")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


# Set PLC port to DOWN
print("Setting PLC port to DOWN: ", end="", flush=True)
cmds = [
    "config switch physical-port",
    "edit port3",
    "set status down",
    "end"
]
exec_ssh_cmds(cmds)
print(f"[{Fore.GREEN}DONE{Style.RESET_ALL}]")


# Set IP to PLC's IP
print("Setting local IP to PLC IP: ", end="", flush=True)
set_ip(interface, targetaddr, targetsubnet, targetgateway)
print(f"[{Fore.GREEN}DONE{Style.RESET_ALL}]")

print("Waiting for IP to kick in: ", end="", flush=True)
time.sleep(2)
print(f"[{Fore.GREEN}DONE{Style.RESET_ALL}]")


# Run modbus server
print("Starting modbus server: ", end="", flush=True)
server = ModbusServer(host="0.0.0.0", port=502)
DataBank.set_bits(0, [1, 1, 1, 1, 1, 1, 1, 1, 1])
DataBank.set_words(0, [2**15-1, 2**15-1, 2**15-1, 2**15-1,
                       2**15-1, 2**15-1, 2**15-1, 2**15-1, 2**15-1, 2**15-1])
print(f"[{Fore.GREEN}DONE{Style.RESET_ALL}]")
print("Press Ctrl+C to safely stop server")
server.start()
