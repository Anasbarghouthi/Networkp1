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

client_socket1 = socket(AF_INET, SOCK_DGRAM)
client_socket1.connect((host, udp_port))
print (f"connected as {client_name}")
client_socket1.sendto(client_name.encode(),(host,udp_port))
print ("UDP connection established ")




#?print instruction of game...
data = client_socket.recv(1024).decode()  # receive response
print (data)

modifiedMessage = ""


#UDP sending 
while modifiedMessage != "Correct":
    check_massage=client_name
    client_socket.send(check_massage.encode())

    message = input("Enter your guess: ")  
    client_socket1.sendto(message.encode(),(host,udp_port))
    modifiedMessage, _ = client_socket1.recvfrom(4096)
    modifiedMessage=modifiedMessage.decode()
    if len(modifiedMessage) > 10 :
         print (modifiedMessage)
    else:      
         print("Feedback", modifiedMessage)
         

    x = client_socket.recv(1024).decode()  # receive response
    a = client_socket.recv(1024).decode()  # receive response 
    

    if a != "none": 
        if a == "time out": 
            print("Time out \n======= LOSER =======") 
            break
        elif a !="You won" and modifiedMessage == "Correct":
             print (f"yes your guess is right but you too late {a} won ")
             break
        elif  a == "You won": 
            print("======= WINNER =======")
            break
        elif a == "you are alone":
             yes_or_no=input("you are alone do you want to continue / ( yes , no ) ")
             client_socket.send(yes_or_no.encode())
             if yes_or_no =="no":
                print("======= WINNER =======")
                print (f"Target number was : {x}")
                break

        else: 
            print("=== GAME RESULTS ===") 
            print (f"Target number was : {x}")
            print("The winner is:", a)
            break

    time.sleep(10.0) 


client_socket.close()  # close the connection
client_socket1.close()

