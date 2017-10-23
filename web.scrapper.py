# Dials the Phone, not sending any DATA

import socket 

# Create End Point on my computer to be "READY" to be connected to the Far End
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Pass HOST(domain Name) and Port 
mysock.connect( ('data.pr4e.org', 80) )

cmd = 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\n\n'.encode()
mysock.send(cmd)

while True:
	data = mysock.recv(512)
	if (len(data) < 1):
		break
	print(data.decode())
mysock.close()

# Hypertext Transfer Protocol (HTTP)
# rfc2616
# Telnet - prehistoric software - connect to any server 