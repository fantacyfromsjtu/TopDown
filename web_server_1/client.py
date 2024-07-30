"""不使用浏览器，编写自己的HTTP客户端来测试你的服务器。您的客户端将使用一个TCP连接用于连接到服务器，向服务器发送HTTP请求，并将服务器响应显示出来。您可以假定发送的HTTP请求将使用GET方法。
客户端应使用命令行参数指定服务器IP地址或主机名，服务器正在监听的端口，以及被请求对象在服务器上的路径。以下是运行客户端的输入命令格式。 

> client.py server_host server_port filename"""
from socket import *
import os
import sys

if len(sys.argv) != 4:
    print("Usage: client.py server_host server_port filename")
    sys.exit(1)
    
serverName = sys.argv[1]
serverPort = int(sys.argv[2])
fileName = sys.argv[3]

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

#构造HTTP报文

request = f"GET /{fileName} HTTP/1.1\r\nHost: {serverName}\r\n\r\n"

clientSocket.send(request.encode())


# 初始化一个变量用于存储完整的响应
response = b''

# 循环接收响应数据，直到数据读取完毕
while True:
    part = clientSocket.recv(1024)
    if not part:
        break
    response += part

clientSocket.close()

# 打印完整的响应内容
print(response.decode())