#dns udp server
import socket
from dnslib import DNSRecord

def parsed_data(data):
#the format im using for this is: "zz1.data.xx1.ns.example.com"
    parsed_data = data[data.index("zz1."):data.index(".xx1")].replace("zz1.","").replace(".xx1","")
    return parsed_data
server = ""
udoser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udoser.bind((server, 53))
i=0
while i == 0:
    recv_data = udoser.recv(2048)
    if recv_data == None:
        break
    d = DNSRecord.parse(recv_data) #unpack the data
    print parsed_data(str(d)) #parse and print data
