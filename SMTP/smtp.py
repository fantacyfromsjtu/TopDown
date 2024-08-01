from socket import *
import ssl

subject = "Hello World!"
contenttype = "text/plain"
msg = "\r\n Hello World!"
endmsg = "\r\n.\r\n"

# Sender and reciever
fromaddress = "13625180036@163.com"
toaddress = "1615999634@qq.com"

# SMTP服务器地址和端口
mailserver = "smtp.163.com"
serverPort = 25

# 创建TCP连接
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, serverPort))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')
for i in range(10):
    # 创建TCP连接
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, serverPort))

    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')
    # 发送HELO命令并接收响应
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # 发送AUTH LOGIN命令进行身份验证
    authCommand = 'AUTH LOGIN\r\n'
    clientSocket.send(authCommand.encode())
    recv2 = clientSocket.recv(1024).decode()
    print(recv2)
    if recv2[:3] != '334':
        print('334 reply not received from server.')

    # 发送Base64编码的用户名，确保末尾有换行符
    username = "MTM2MjUxODAwMzY="  # 你的用户名的Base64编码
    clientSocket.send((username + "\r\n").encode())
    recv3 = clientSocket.recv(1024).decode()
    print(recv3)
    if recv3[:3] != '334':
        print('334 reply not received from server.')

    # 发送Base64编码的密码，确保末尾有换行符
    password = "VVJMSldLVEhXRlFDR1hZQg=="  # 你的密码的Base64编码
    clientSocket.send((password + "\r\n").encode())
    recv4 = clientSocket.recv(1024).decode()
    print(recv4)
    if recv4[:3] != '235':
        print('235 reply not received from server.')

    # 发送MAIL FROM命令
    MailFrom = f'MAIL FROM: <{fromaddress}>\r\n'
    clientSocket.send(MailFrom.encode())
    recv5 = clientSocket.recv(1024).decode()
    print(recv5)
    if recv5[:3] != '250':
        print('250 reply not received from server.')

    # 发送RCPT TO命令
    RCPT = f'RCPT TO: <{toaddress}>\r\n'
    clientSocket.send(RCPT.encode())
    recv6 = clientSocket.recv(1024).decode()
    print(recv6)
    if recv6[:3] != '250':
        print('250 reply not received from server.')

    # 发送DATA命令
    DATA = 'DATA\r\n'
    clientSocket.send(DATA.encode())
    recv7 = clientSocket.recv(1024).decode()
    print(recv7)
    if recv7[:3] != '354':
        print('354 reply not received from server.')

    # 发送邮件内容
    message = f'from:{fromaddress}\r\n'
    message += f'to:{toaddress}\r\n'
    message += f'subject:{subject}\r\n'
    message += f'Content-Type:{contenttype}\r\n'
    message += '\r\n' + msg
    clientSocket.send(message.encode())

    # 发送结束标识
    clientSocket.send(endmsg.encode())
    recv8 = clientSocket.recv(1024).decode()
    print(recv8)
    if recv8[:3] != '250':
        print('250 reply not received from server.')

    # 发送QUIT命令
    Quit = 'QUIT\r\n'
    clientSocket.send(Quit.encode())
    recv9 = clientSocket.recv(1024).decode()
    print(recv9)
    if recv9[:3] != '221':
        print('221 reply not received from server.')

clientSocket.close()
