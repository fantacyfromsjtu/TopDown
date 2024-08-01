from socket import *
import ssl

subject = "Hello World!"
contenttype = "text/plain"
msg = "\r\n Hello World!"
endmsg = "\r\n.\r\n"

# Sender and receiver
fromaddress = "13625180036@163.com"
toaddress = "haocong-he@sjtu.edu.cn"

# SMTP服务器地址和端口
mailserver = "smtp.163.com"
serverPort = 25  # 对于TLS，初始连接到非安全端口

# 创建TCP连接
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, serverPort))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# 发送EHLO命令
heloCommand = 'EHLO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# 检查服务器是否支持STARTTLS
if "STARTTLS" not in recv1:
    print('STARTTLS not supported by server.')
    clientSocket.close()
    exit()

# 发送STARTTLS命令以启动TLS
starttlsCommand = 'STARTTLS\r\n'
clientSocket.send(starttlsCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '220':
    print('220 reply not received from server.')

# 使用SSL包装套接字
context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)

# 重新发送EHLO命令
clientSocket.send(heloCommand.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')

# 发送AUTH LOGIN命令进行身份验证
authCommand = 'AUTH LOGIN\r\n'
clientSocket.send(authCommand.encode())
recv4 = clientSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '334':
    print('334 reply not received from server.')

# 发送Base64编码的用户名，确保末尾有换行符
username = "MTM2MjUxODAwMzY="  # 你的用户名的Base64编码
clientSocket.send((username + "\r\n").encode())
recv5 = clientSocket.recv(1024).decode()
print(recv5)
if recv5[:3] != '334':
    print('334 reply not received from server.')

# 发送Base64编码的密码，确保末尾有换行符
password = "VVJMSldLVEhXRlFDR1hZQg=="  # 你的密码的Base64编码
clientSocket.send((password + "\r\n").encode())
recv6 = clientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '235':
    print('235 reply not received from server.')

# 发送MAIL FROM命令
MailFrom = f'MAIL FROM: <{fromaddress}>\r\n'
clientSocket.send(MailFrom.encode())
recv7 = clientSocket.recv(1024).decode()
print(recv7)
if recv7[:3] != '250':
    print('250 reply not received from server.')

# 发送RCPT TO命令
RCPT = f'RCPT TO: <{toaddress}>\r\n'
clientSocket.send(RCPT.encode())
recv8 = clientSocket.recv(1024).decode()
print(recv8)
if recv8[:3] != '250':
    print('250 reply not received from server.')

# 发送DATA命令
DATA = 'DATA\r\n'
clientSocket.send(DATA.encode())
recv9 = clientSocket.recv(1024).decode()
print(recv9)
if recv9[:3] != '354':
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
recv10 = clientSocket.recv(1024).decode()
print(recv10)
if recv10[:3] != '250':
    print('250 reply not received from server.')

# 发送QUIT命令
Quit = 'QUIT\r\n'
clientSocket.send(Quit.encode())
recv11 = clientSocket.recv(1024).decode()
print(recv11)
if recv11[:3] != '221':
    print('221 reply not received from server.')

clientSocket.close()
