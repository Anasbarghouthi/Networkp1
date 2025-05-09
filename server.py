from socket import *
import time
import random
import threading




player_list=[]
player_udp_addresses = {}
winner=False
winner_name=""
host = gethostname() # get the hostname
tcp_port = 6000
udp_port = 6001 
number_of_player=0
counter=0
lock=threading.Lock()
max_player=2



def guess_random_number(modifiedMessage,client_address):
	
	global winner, winner_name,x
	if not modifiedMessage.isdigit(): 
		return "Please send a valid number."
	
	modifiedMessage=int(modifiedMessage)
	if modifiedMessage > 100 :
		return "Warning: out of the range , miss your chance "
	if (x > modifiedMessage):
		return "Higher"
	elif (x < modifiedMessage):
		return "Lower"
	else :
		if not winner:
			winner=True
			winner_name=player_udp_addresses[client_address]	
		return "Correct"
	
	


	
def program (connectionSocket, address):
	
	global winner, winner_name,number_of_player,counter,max_player
	

	
	try:
		data = connectionSocket.recv(1024).decode()
	except	(ConnectionResetError , ConnectionAbortedError , OSError):
		max_player -=1
		return	

	while True :
			
				t=True 
				for i in player_list:
					if data == i:
						data = " Enter another name that name was used "
						try:
							connectionSocket.send(data.encode())  # send data to the client
							data = connectionSocket.recv(1024).decode()
						except	(ConnectionResetError , ConnectionAbortedError , OSError):
							max_player -=1
							return	
						t=False
						break
				if t:
					player_list.append(data)
					data = "Enter game"
					try:
						connectionSocket.send(data.encode())  # send data to the client
					except	(ConnectionResetError , ConnectionAbortedError , OSError):
						max_player -=1
						return	
					break	
			

	
	
	message, clientAddress = server_socket1.recvfrom(1024)
	if clientAddress[1] not in player_udp_addresses:
			player_udp_addresses[clientAddress[1]] = message.decode()

	print(f"New Connection from: {address} as {data}")
	if number_of_player ==0:
		print ("Starting game with ",max_player,"players")

	with lock:
		number_of_player +=1
	while number_of_player < max_player:
		time.sleep(0.2)

	temp=str(player_list)
	data=f"Game stared with players: {temp} \n you have 60 seconds to guess the number (0-100)!"
	connectionSocket.send(data.encode())

	connectionSocket.send(str(x).encode())

	
	
	start_time=time.time() 
	while True:
		#to check if client still connected 
		
		try:
			client_name = connectionSocket.recv(1024).decode()
		except (timeout,ConnectionResetError , ConnectionAbortedError , OSError):
			if  (clientAddress[1] in player_udp_addresses):
				print (player_udp_addresses[clientAddress[1]] ," is disconnected ")
				number_of_player -=1
				break

		############
			
		# client guess
		try:
			message, clientAddress = server_socket1.recvfrom(1024)
			message=message.decode()
		#send the result to client 
			message=guess_random_number(message,clientAddress[1])
			server_socket1.sendto(message.encode(),clientAddress)
		except (ConnectionResetError , ConnectionAbortedError , OSError):
			continue	
		###############


		# escape if one win or time out or number of player >=1
			
		escape=time.time()-start_time
		try:
			
			if winner:
				if player_udp_addresses[clientAddress[1]] == winner_name:
					a="You won"
				else:
					a=winner_name	
				connectionSocket.send(a.encode())
			elif escape >=60:
				a="time out"
				connectionSocket.send(a.encode())
			elif number_of_player <=1 :
				a="you are alone"
				connectionSocket.send(a.encode())
				yes_or_no=connectionSocket.recv(1024).decode()
				if yes_or_no=="no":
					break
				else:
					number_of_player +=1
			else:
				a="none"
				connectionSocket.send(a.encode())
		except	(ConnectionResetError , ConnectionAbortedError , OSError):
			continue	
						
		if escape >= 60 or winner  or number_of_player <=1 :
			break
		
		
		########################


	connectionSocket.close()  # close the connectionSocketection	

	


x=random.randint(0,100)
max_player=input("Enter the max number of player ")
max_player=int(max_player)
print ("the number is = ",x)
server_socket1 = socket(AF_INET,SOCK_DGRAM)  # get instance
server_socket1.bind((host, udp_port))

server_socket = socket(AF_INET,SOCK_STREAM)  # get instance
server_socket.bind((host, tcp_port))  # bind host address and port together
# configure how many client the server can listen simultaneously #2
print ("Server stared in ",host,":TCP 6000.UDP 6001")
server_socket.listen(4)
thread=[]
for _ in range(max_player):
	connectionSocket, address = server_socket.accept()  # accept new connectionSocketection
	t = threading.Thread(target=program, args=(connectionSocket, address))
	t.start()
	thread.append(t)

for th in thread:
	th.join()
	 

	



	