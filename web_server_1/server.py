#import socket module
from socket import *
import os

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverName = '192.168.124.8'
serverPort = 1145
serverSocket.bind(('', serverPort))
serverSocket.listen(5)

while True:
    # Establish the connection
    print("Ready to serve...")
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        #print(f"Request message: {message}")  # Debug: print the received message
        filename = message.split()[1]
        #print(f"Requested file: {filename}")  # Debug: print the requested filename

        # Open and read the requested file
        with open(filename[1:], 'r') as f:
            outputdata = f.read()

        # Send one HTTP header line into socket
        response_header = 'HTTP/1.1 200 OK\r\n'
        response_header += 'Content-Type: text/html\r\n'
        response_header += f'Content-Length: {len(outputdata)}\r\n'
        response_header += '\r\n'

        connectionSocket.send(response_header.encode())

        # Send the content of the requested file to the client
        connectionSocket.send(outputdata.encode())
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        response_header = 'HTTP/1.1 404 Not Found\r\n'
        response_header += 'Content-Type: text/html\r\n'
        response_header += '\r\n'
        connectionSocket.send(response_header.encode())

        # Close client socket
        connectionSocket.close()

        # Debug: print error message
        #print(f"Error: file not found {filename[1:]}")
    except Exception as e:
        # Catch other exceptions and print the error message
        print(f"Unexpected error: {e}")
        connectionSocket.close()

# Ensure server socket is closed when server is stopped
serverSocket.close()
