from socket import *
import sys


if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# 创建一个服务器套接字，绑定到指定端口并开始监听
tcpSerSock = socket(AF_INET, SOCK_STREAM)
serverPort = 12000  # 服务器使用的端口
tcpSerSock.bind(('', serverPort))  # 绑定端口
tcpSerSock.listen(10)  # 开始监听传入的连接请求

cache = {}  # 用于缓存的字典


def handle_request(tcpCliSock):
    try:
        # 接收客户端的请求消息
        message = tcpCliSock.recv(4096).decode()
        print(message)

        # 提取请求方法和URL
        method = message.split()[0]  # 获取请求方法（例如GET或POST）
        url = message.split()[1]  # 获取请求的URL
        hostn = url.split('/')[2]  # 提取主机名
        path = '/' + '/'.join(url.split('/')[3:])  # 构建请求路径
        filename = url.replace("http://", "").replace("/", "_").replace(":", "_")  # 构建缓存文件名
        print(path)
        print(filename)

        # 处理GET请求
        if method == "GET":
            if filename in cache:
                print('Cache hit')
                with open(filename, "rb") as f:
                    outputdata = f.read()
                    tcpCliSock.sendall("HTTP/1.0 200 OK\r\n".encode())
                    tcpCliSock.sendall("Content-Type:text/html\r\n\r\n".encode())
                    tcpCliSock.sendall(outputdata)
                print('Read from cache')
            else:
                print('Cache miss')
                fetch_from_server(tcpCliSock, hostn, path, filename)
        # 处理POST请求
        elif method == "POST":
            headers = message.split("\r\n\r\n")[0]  # 提取请求头
            body = message.split("\r\n\r\n")[1]  # 提取请求体
            fetch_from_server(tcpCliSock, hostn, path, filename, method, headers, body)
        else:
            tcpCliSock.sendall("HTTP/1.0 501 Not Implemented\r\n\r\n".encode())  # 处理未实现的方法
    except Exception as e:
        print("Error handling request:", e)
        tcpCliSock.sendall("HTTP/1.0 400 Bad Request\r\n\r\n".encode())
    finally:
        tcpCliSock.close()  # 关闭客户端连接


def fetch_from_server(tcpCliSock, hostn, path, filename, method="GET", headers=None, body=None):
    try:
        c = socket(AF_INET, SOCK_STREAM)  # 创建一个新的套接字用于连接目标服务器
        c.connect((hostn, 80))  # 连接到目标服务器的80端口
        if method == "GET":
            request_line = f"GET {path} HTTP/1.0\r\nHost: {hostn}\r\n\r\n"
        elif method == "POST":
            request_line = f"POST {path} HTTP/1.0\r\nHost: {hostn}\r\n{headers}\r\n\r\n{body}"
        c.sendall(request_line.encode())  # 发送请求行和头信息
        response = b""  # 初始化空的响应变量
        while True:
            data = c.recv(4096)  # 从服务器接收数据
            if len(data) > 0:
                response += data  # 累积响应数据
            else:
                break  # 如果没有更多数据，则退出循环

        # 检查响应状态码
        if b"404 Not Found" in response:
            tcpCliSock.sendall("HTTP/1.0 404 Not Found\r\n\r\n".encode())
        else:
            tcpCliSock.sendall(response)  # 将响应数据发送给客户端
            if "200 OK" in response.decode():  # 如果响应中包含200 OK
                with open(filename, "wb") as tmpFile:
                    tmpFile.write(response)  # 将响应数据写入缓存文件
                cache[filename] = True  # 更新缓存字典
        c.close()  # 关闭与目标服务器的连接
    except Exception as e:
        print("Illegal request:", e)
        tcpCliSock.sendall("HTTP/1.0 400 Bad Request\r\n\r\n".encode())  # 处理非法请求


while True:
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()  # 接受客户端连接
    print('Received a connection from:', addr)
    handle_request(tcpCliSock)  # 处理客户端请求
