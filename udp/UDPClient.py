from socket import *

serverName = '192.168.32.143'    # The server's hostname or IP address   
serverPort = 12000           # The port used by the server
clientSocket = socket(AF_INET, SOCK_DGRAM)   # Create a UDP socket
message = input('Input lowercase sentence: ')   # Take input from user
clientSocket.sendto(message.encode(), (serverName, serverPort))   # Send message to server
modifyedMessage, serverAddress = clientSocket.recvfrom(2048)   # Receive message from server
print(modifyedMessage.decode())
clientSocket.close()