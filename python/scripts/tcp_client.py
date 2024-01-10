#!/usr/bin/env python
#!/usr/bin/python3

"""
TCP Client

Assumptions:
- connection will always succeed
- the server expects data first
- the server will always return data in a timely fashion
"""

import socket

# target_host = "www.google.com"
# target_port = 80
target_host = '0.0.0.0'
target_port = 9998

# create socket object
#   AF_INET indicates use of standard IPv4 address or hostname
#   SOCK_STREAM indicates TCP client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host, target_port))

# send some data (as bytes)
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# receive some data
response = client.recv(4096)

print(response.decode())
client.close()
