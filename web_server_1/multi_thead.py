from socket import *
import os
from threading import Thread

def main():
    serverPort = 1145
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(10)
    print("Server is ready to serve...")

    while True:
        connectionSocket, addr = serverSocket.accept()
        print(f"Connection from {addr}")
        # 创建新线程处理客户端请求
        connect_thread = Thread(target=TCPconnection, args=(connectionSocket, addr))
        connect_thread.start()

def TCPconnection(connectionSocket, addr):
    try:
        message = connectionSocket.recv(1024).decode()
        print(f"Request message: {message}")  # Debug: print the received message
        filename = message.split()[1]
        print(f"Requested file: {filename}")  # Debug: print the requested filename

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
    except IOError:
        # Send response message for file not found
        response_header = 'HTTP/1.1 404 Not Found\r\n'
        response_header += 'Content-Type: text/html\r\n'
        response_header += '\r\n'
        try:
            connectionSocket.send(response_header.encode())
        except OSError as e:
            print(f"Error sending 404 response: {e}")
        # Debug: print error message
        print(f"Error: file not found {filename[1:]}")
    except Exception as e:
        # Catch other exceptions and print the error message
        print(f"Unexpected error: {e}")
    finally:
        # Close client socket
        try:
            connectionSocket.close()
        except OSError as e:
            print(f"Error closing socket: {e}")

if __name__ == "__main__":
    main()
