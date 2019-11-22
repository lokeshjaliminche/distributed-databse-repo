#!/usr/bin/python3

import socket
import sys
from threading import Thread

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = int(sys.argv[1])

# connection to hostname on the port.
s.connect((host, port))                               

s.send(b'STX')
# Receive no more than 1024 bytes
msg = s.recv(1024)                                     

s.close()
print (msg)

