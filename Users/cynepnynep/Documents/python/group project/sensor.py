#!/usr/bin/python3
import argparse
import time
import logging
import os.path
import socket as sckt
import sys
import Adafruit_DHT as dht
from datetime import datetime
from threading import Thread


class mainClass():

	def argPrse():

		prsr = argparse.ArgumentParser(description='activate angie server')
		prsr.add_argument('port', help='specify the port number (defaults to 60606)',
							nargs='?', default=60606, type=int)
		prsr.add_argument("-l", "--log", help='specify log level (defaults to INFO)',
							nargs='?', default='INFO')

		args = prsr.parse_args()
		logLvl = args.log
		port = args.port
		return(logLvl, port)

	def preStp(logLvl):

		home = str(os.environ['HOME'])
		wrkDir = str(os.path.dirname(os.path.realpath(sys.argv[0])))
		cache = str("{}/.cache/angie".format(home))
		if not os.path.exists(cache):
			os.makedirs(cache)
			#logging.info('created \'thServer\' directory under {}/.cache'.format(home)) # this requires smart workaround, have previously verified solution ready, would prefer to figure out a different one this time
		logFile = str("{}/.cache/angie/angie.log".format(home))
		logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
							datefmt='%y%b%d%a%I%M%S%p', filename=logFile, level=logLvl)

	def scktStp(port):

		srvrSckt = sckt.socket(sckt.AF_INET, sckt.SOCK_STREAM)
		srvrSckt.setsockopt(sckt.SOL_SOCKET, sckt.SO_REUSEADDR, 1)
		srvrSckt.bind(192.168.1.11, port)
		srvrSckt.listen(port)
		return(srvrSckt)

	def mainFunc(srvrSckt):
		
		
		def clntFunc(scktInc, rmtePort):
			
			try:
				while True:
					sensor = 11
					pin = 14
					humidity, temperature = dht.read_retry(sensor, pin)
					if (humidity is not None) and (temperature is not None):
						nowtime = datetime.strftime(datetime.now(), "%d.%m %H:%M:%S")
						temperature = str(temperature)
						humidity = str(humidity)
						msg_out = (nowtime + "\t" + temperature + "C\t" + humidity +"%")
						data_out = msg_out.encode()
						srvrSckt.send(data_out)
						time.sleep(300)
			except TabError:
				print('error')
				
		  
		try:
			n = 1
			while True:
				scktInc, rmtePort = srvrSckt.accept()
				print("starting thread {}..".format(n))
				clntThrd = Thread(target=clntFunc, args=(scktInc, rmtePort))
				print(str(scktInc), str(rmtePort))
				clntThrd.start()
				n += 1
		except KeyboardInterrupt:
			print("\nuser interrupt")

		if n != 1:
			print("socket evironment cleanup..")
			scktInc.shutdown(sckt.SHUT_RDWR)
			scktInc.close()

	# parse arguments
	logLvl, port = argPrse()
	portnum = port
	# act
	preStp(logLvl)
	srvrSckt = scktStp(port)
	print(str(port))
	mainFunc(srvrSckt)
	# done - exit
	print("exit")
	exit(0)

if __name__ == "main":
	mainClass()
