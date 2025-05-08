from socket import *
import time
import random
import threading
import copy




player_list=[]
player_udp_addresses = {}
winner=False
winner_name=""
host = gethostname() # get the hostname
tcp_port = 6000
udp_port = 6001 
number_of_player=0
counter=0



def guess_random_number(modifiedMessage,client_address):
	
	global winner, winner_name,x
	if winner :
		return "There is a winner"
	if not modifiedMessage.isdigit(): 
		return "Please send a valid number."
	
	modifiedMessage=int(modifiedMessage)
	if (x > modifiedMessage):
		return "Higher"
	elif (x < modifiedMessage):
		return "Lower"
	else :
		winner=True
		winner_name=player_udp_addresses[client_address]
		return "Correct"
	
	


	
def program (connectionSocket, address):
	
	global winner, winner_name,number_of_player,counter
	

	print(f"Connection from: {address}")

	data = connectionSocket.recv(1024).decode()
	while True :
			t=True 
			for i in player_list:
				if data == i:
					data = " Enter another name that name was used "
					connectionSocket.send(data.encode())  # send data to the client
					data = connectionSocket.recv(1024).decode()
					t=False
					break
			if t:
				player_list.append(data)
				data = "Enter game"
				connectionSocket.send(data.encode())  # send data to the client
				break	

	
	
	message, clientAddress = server_socket1.recvfrom(1024)
	if clientAddress[1] not in player_udp_addresses:
			player_udp_addresses[clientAddress[1]] = message.decode()

	number_of_player +=1
	while number_of_player < 2:
		time.sleep(0.2)


	connectionSocket.send(data.encode())
	
	
	start_time=time.time() 

	
	print (player_udp_addresses)
	while True:
		#to check if client still connected 
		client_name = connectionSocket.recv(1024).decode()
		if (not client_name) and (clientAddress[1] in player_udp_addresses):
			print (player_udp_addresses[clientAddress[1]] ," is disconnected ")
		############
			
		# client guess
		message, clientAddress = server_socket1.recvfrom(1024)
		message=message.decode()
		
		

		#send the result to client 
		message=guess_random_number(message,clientAddress[1])
		server_socket1.sendto(message.encode(),clientAddress)
		###############


		# escape if one win or time out or number of player >=1
		
		escape=time.time()-start_time
		print (winner)
		if escape >= 60 or winner :
			break
		
		
		########################

	
	
	counter +=1
	while counter < number_of_player :
		time.sleep(0.2)
		
	
	if winner:
		data = winner_name
		connectionSocket.send(data.encode())  # send data to the client
	elif number_of_player <= 1 :
		data = " === the another player disconnect === \n  you are the winner "
		connectionSocket.send(data.encode())  # send data to the client
	else:
		data = " === Everyone lost =="
		connectionSocket.send(data.encode())  # send data to the client

		
	connectionSocket.close()  # close the connectionSocketection	

	


x=random.randint(0,100)
print ("the number is = ",x)
server_socket1 = socket(AF_INET,SOCK_DGRAM)  # get instance
server_socket1.bind((host, udp_port))

server_socket = socket(AF_INET,SOCK_STREAM)  # get instance
server_socket.bind((host, tcp_port))  # bind host address and port together
# configure how many client the server can listen simultaneously #2
server_socket.listen(4)
thread=[]
for _ in range(2):
	connectionSocket, address = server_socket.accept()  # accept new connectionSocketection
	t = threading.Thread(target=program, args=(connectionSocket, address))
	t.start()
	thread.append(t)

for th in thread:
	th.join()
	 


# while True:
# 	if number_of_player <= 4:
# 		connectionSocket, address = server_socket.accept()  # accept new connectionSocketection
# 		t = threading.Thread(target=program, args=(connectionSocket, address))
# 		t.start()
# 	else:
# 		print ("Maximum number of players reached. No more connections accepted.")
# 		break	



	