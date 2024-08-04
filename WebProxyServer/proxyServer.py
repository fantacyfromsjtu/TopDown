from socket import *  # 导入socket模块
import sys  # 导入sys模块


# 检查命令行参数是否少于或等于1，如果是则提示使用方法并退出
if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# 创建一个服务器套接字，绑定到指定端口并开始监听
tcpSerSock = socket(AF_INET, SOCK_STREAM)
serverPort = 12000  # 服务器使用的端口
tcpSerSock.bind(('', serverPort))  # 绑定端口
tcpSerSock.listen(10)  # 开始监听传入的连接请求

while True:
    print('Ready to serve...')

    # 接受客户端的连接
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    try:
        # 接收客户端的请求消息
        message = tcpCliSock.recv(4096).decode()
        print(message)

        # 从请求消息中提取URL和文件名
        url = message.split()[1]  # 获取请求的URL
        hostn = url.split('/')[2]  # 提取主机名
        path = '/' + '/'.join(url.split('/')[3:])  # 构建请求路径
        filename = url.replace("http://", "").replace("/", "_").replace(":", "_")  # 构建缓存文件名
        print(path)
        print(filename)

        fileExist = "false"
        filetouse = filename
        print(filetouse)

        try:
            # 检查缓存文件是否存在
            with open(filetouse, "rb") as f:
                outputdata = f.read().replace(b"\r\n", b"\r")
                fileExist = "true"
                # 如果缓存文件存在，返回缓存内容
                tcpCliSock.sendall("HTTP/1.0 200 OK\r\n".encode())
                tcpCliSock.sendall("Content-Type:text/html\r\n\r\n".encode())
                tcpCliSock.sendall(outputdata)
            print('Read from cache')

        except IOError:
            # 如果缓存文件不存在，从远程服务器获取数据
            if fileExist == "false":
                c = socket(AF_INET, SOCK_STREAM)
                print(hostn)

                try:
                    # 连接到目标服务器的80端口
                    c.connect((hostn, 80))

                    # 创建并发送请求给目标服务器
                    request_line = f"GET {path} HTTP/1.0\r\nHost: {hostn}\r\n\r\n"
                    c.sendall(request_line.encode())

                    # 从目标服务器读取响应数据
                    response = b""
                    while True:
                        data = c.recv(4096)
                        if len(data) > 0:
                            response += data
                        else:
                            break
                    # 将响应数据发送给客户端
                    tcpCliSock.sendall(response)

                    # 将响应数据缓存到本地文件
                    with open(filetouse, "wb") as tmpFile:
                        tmpFile.write(response.replace(b"\r\n", b"\r"))

                    c.close()
                except Exception as e:
                    print("Illegal request:", e)
                    try:
                        tcpCliSock.sendall("HTTP/1.0 400 Bad Request\r\n\r\n".encode())
                    except Exception as send_err:
                        print("Error sending error message to client:", send_err)
            else:
                try:
                    tcpCliSock.sendall("HTTP/1.0 404 Not Found\r\n\r\n".encode())
                except Exception as send_err:
                    print("Error sending 404 message to client:", send_err)

    except Exception as e:
        print("Error handling request:", e)

    finally:
        # 关闭客户端连接
        tcpCliSock.close()
