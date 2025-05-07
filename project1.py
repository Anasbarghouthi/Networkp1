from socket import *
import time
tcp_port = 6000  # socket server port number
host = gethostname()  # as both code is running on same pc
udp_port=6001


client_socket = socket(AF_INET,SOCK_STREAM)  # instantiate
client_socket.connect((host, tcp_port))  # connect to the server
message = input(" Enter your name: ")  # take input
data=" "
while data.lower().strip() != 'Enter game':
	client_socket.send(message.encode())  # send message
	data = client_socket.recv(1024).decode()  # receive response
	if data == 'Enter game':
		break
	message = input("Enter new  name:")  # again take input
#client_socket.close()  # close the connection


data = client_socket.recv(1024).decode()  # receive response


client_socket1 = socket(AF_INET, SOCK_DGRAM)
client_socket1.connect((host, udp_port))

modifiedMessage = ""
while modifiedMessage != "winner": 
    message = input("Enter your guess: ")  
    client_socket1.send(message.encode())  
    modifiedMessage = client_socket1.recv(1024).decode()  
    print("Feedback", modifiedMessage) 
    if modifiedMessage == "There is a winner": 
        break 
    time.sleep(10.0) 



	
client_socket1.close()




#client_socket = socket(AF_INET,SOCK_STREAM)  # instantiate
#client_socket.connect((host, tcp_port))  # connect to the server
data = client_socket.recv(1024).decode()  # receive response
print (data)
data = client_socket.recv(1024).decode()  # receive response
print (data)
client_socket.close()  # close the connection


