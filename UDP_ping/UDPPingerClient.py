from socket import *
import time

Count = 10
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)  # 设置超时时间为1秒
lost = 0
RTTtime = []

for i in range(Count):
    startTime = time.perf_counter()
    message = 'Ping ' + str(i+1) + ' ' + str(startTime)
    clientSocket.sendto(message.encode(), (serverName, serverPort))   # 发送消息到服务器

    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)  # 从服务器接收消息
        endTime = time.perf_counter()
        rtt = endTime - startTime
        RTTtime.append(rtt)
        print(f"RTT: {rtt:.6f} s")
        print(modifiedMessage.decode())
    except timeout:
        lost += 1
        print('Timeout!')

clientSocket.close()
minTime = min(RTTtime)
maxTime = max(RTTtime)
avgTime = sum(RTTtime) / len(RTTtime)
lostRate = lost / Count 

print('==========================')
print(f"minTime: {minTime:.6f} s")
print(f"maxTime: {maxTime:.6f} s")
print(f"avgTime: {avgTime:.6f} s")
print("Lost Rate: " + str(lostRate * 100) + '%')