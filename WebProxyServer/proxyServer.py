from socket import *
import sys
import os

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
serverPort = 12000  # The port used by the server
tcpSerSock.bind(('', serverPort))
tcpSerSock.listen(10)  # Listen for incoming connections

while 1:
    print('Ready to serve...')

    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    message = tcpCliSock.recv(4096).decode()
    print(message)

    # Extract the filename from the given message
    url = message.split()[1]
    filename = url.partition("/")[2]
    print(filename)

    fileExist = "false"
    filetouse = "/" + filename.replace("/", "_")
    print(filetouse)

    try:
        # Check whether the file exists in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.read().replace("\r\n", "\r").splitlines(True)
        fileExist = "true"
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n".encode())
        for line in outputdata:
            tcpCliSock.send(line.encode())
        print('Read from cache')

    except IOError:
        if fileExist == "false":
            c = socket(AF_INET, SOCK_STREAM)
            hostn = url.split('/')[2]
            print(hostn)

            try:
                # Connect to the target server on port 80
                c.connect((hostn, 80))

                # Create and send the request to the target server
                request_line = f"GET /{'/'.join(filename.split('/')[1:])} HTTP/1.0\r\nHost: {hostn}\r\n\r\n"
                c.send(request_line.encode())

                # Read the response from the target server
                response = b""
                while True:
                    data = c.recv(4096)
                    if len(data) > 0:
                        response += data
                    else:
                        break
                tcpCliSock.send(response)

                # Cache the response
                with open(filetouse[1:], "wb") as tmpFile:
                    tmpFile.write(response.replace(b"\r\n", b"\r"))

                c.close()
            except Exception as e:
                print("Illegal request:", e)
                tcpCliSock.send("HTTP/1.0 400 Bad Request\r\n\r\n".encode())
        else:
            tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode())

    tcpCliSock.close()
