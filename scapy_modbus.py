from scapy.all import *
from scapy.layers.inet import *

sport = random.randint(1024, 65535)

# SYN
ip = IP(dst="192.168.1.32", src="192.168.1.250")  # src="192.168.1.246"
eth = Ether(dst="00:80:f4:4e:3a:4c")  # src="a8:74:1d:86:8c:cb",
SYN = TCP(sport=sport, dport=502, flags='S', seq=1000)
SYNACK = sr1(ip/SYN)

# ACK
ACK = TCP(sport=sport, dport=502, flags='A',
          seq=SYNACK.ack, ack=SYNACK.seq + 1)
send(ip/ACK)

send(ip / TCP(dport=502, sport=sport, seq=SYNACK.ack, ack=SYNACK.seq + 1, flags="AP") /
     Raw(load="\x5c\x07\x00\x00\x00\x06\x01\x06\x00\x01\x00\x00"), iface="Ethernet 2")
