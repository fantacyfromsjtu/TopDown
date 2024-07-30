from socket import *

serverName = '192.168.32.143'    # The server's hostname or IP address
serverPort = 12000           # The port used by the server
clientSocket = socket(AF_INET,SOCK_STREAM)   # Create a TCP socket
clientSocket.connect((serverName,serverPort))   # Connect to server

message = input('Input lowercase sentence: ')   # Take input from user
clientSocket.send(message.encode())   # Send message to server
modifyedMessage = clientSocket.recv(1024)   # Receive message from server
print('From Server:', modifyedMessage.decode())
clientSocket.close()