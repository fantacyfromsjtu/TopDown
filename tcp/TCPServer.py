from socket import *

serverName = '192.168.32.143'    # The server's hostname or IP address
serverPort = 12000           # The port used by the server
serverSocket = socket(AF_INET,SOCK_STREAM)   # Create a TCP socket
serverSocket.bind(('',serverPort))
serverSocket.listen(1)   # Listen for incoming connections
print('The server is ready to receive')
while True:
    connectionSocket,addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    modified = sentence.upper()
    connectionSocket.send(modified.encode())
    connectionSocket.close()