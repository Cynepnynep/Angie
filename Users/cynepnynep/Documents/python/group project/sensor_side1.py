
import socket as sk

#Create a socket
temp1_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

#Set the socket option to reuse the address 
temp1_socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

#Bind to an unused port
port = 64646

#Listen for connections
temp1_socket.listen(port)

#Print message that the server has started. 
print('Temperature1 host listening on port ', port)

#Accept a connection from the client
connection,controller_address = temp1_socket.accept()

#Print the address associated with the client.
print('Echo server on port ', port,  ' has connection with ', controller_address)

#finished = False 
finished = False

#while not finished
while True:
	
	
	data_in = cli_sock.recv(1024)
				#decode data to human readable message
	answer = data_in.decode()
	
	if request = "request":
		
        #get data from pin X (pin_data = data at pin Y)
        pin_data = read.retry(sensor, pin)

        #data out = encode message
		temperature_response = pin_data.encode()

        #Send data out
		connection.send(temperature_response)
   
        
    else:
		
		break
#Shutdown the connection 
connection.shutdown(sk.SHUT_RDWR)

#Close the connection
connection.close()

#Shutdown the server socket 
temp1_socket.shutdown(sk.SHUT_RDWR)

#Close the server socket
temp1_socket.close()
