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
	client_socket.send(message.encode())
	data = client_socket.recv(1024).decode()  # receive response
	if data == 'Enter game':
		break
	message = input("Enter new  name:")  # again take input

client_name=message

data = client_socket.recv(1024).decode()  # receive response


client_socket1 = socket(AF_INET, SOCK_DGRAM)
client_socket1.connect((host, udp_port))

modifiedMessage = ""

#UDP sending 
while modifiedMessage != "winner" and modifiedMessage != "There is a winner":
    check_massage=client_name
    client_socket.send(check_massage.encode())
    dis_client=client_socket.recv(1024).decode()
    if dis_client != "" :
        dis_client=input (dis_client," disconnected do you want to continue . enter yes")
        if dis_client !="yes" :
              break 
    client_socket.send(dis_client.encode())

    message = input("Enter your guess: ")  
    client_socket1.sendto(message.encode(),(host,udp_port))
    modifiedMessage, _ = client_socket1.recvfrom(1024)
    modifiedMessage=modifiedMessage.decode()

    print("Feedback", modifiedMessage) 
    number_of_player = client_socket.recv(1024).decode()
    number_of_player=int (number_of_player)
    if number_of_player <= 1  or modifiedMessage == "There is a winner" or modifiedMessage == "winner":
          break
    time.sleep(10.0) 



	
client_socket1.close()




print ("===GAME RESULTS===\n")
data = client_socket.recv(1024).decode()  # receive response
print (data)
client_socket.close()  # close the connection


