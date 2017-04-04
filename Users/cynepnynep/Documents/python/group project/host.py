#!/usr/bin/python3
import socket as sk
from sys import argv
from datetime import datetime
import shelve
cli_sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
if len(argv) > 1:
	port = int(argv[1])
linked = False
try:
	while not linked:
		try:
			while True:
				cli_sock.connect(('localhost', port))
				linked = True
				print("established connection with port: ", port)
				while True:
						data_in = cli_sock.recv(1024)
						answer = data_in.decode()
						print('received from server: ', answer)
						nowtime = datetime.strftime(datetime.now(), "%d.%m %H:%M:%S")
						datalog = shelve.open(datafile.db)
						datalog[nowtime] = answer
						datalog.close()
		except ConnectionRefusedError:
			print("if you want to exit session input port 0")
			port = int(input('Enter port you want to connect: '))
		except OverflowError:
			print('the number of port for connection must be less then 65536')
			port = int(input('Enter port you want to connect: '))	
except OSError:				
	cli_sock.shutdown(sk.SHUT_RDWR)
	cli_sock.close()
