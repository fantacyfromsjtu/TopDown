import random 
from socket import * 
import time

# Create a UDP socket  
serverSocket = socket(AF_INET, SOCK_DGRAM) 
# Assign IP address and port number to socket 
serverSocket.bind(('', 12000))

lastTime = time.time() 
sequenceNumber = -1

while True:
    currentTime = time.time()
    if currentTime - lastTime > 10:
        print("No heartbeat received in the last 10 seconds. Assuming client has stopped.")
        exit(0)

    try:
        serverSocket.settimeout(1)
        message, address = serverSocket.recvfrom(1024)
        lastTime = currentTime
        recvTime = time.perf_counter()
        
        # Decode the received message
        decodedMessage = message.decode()
        parts = decodedMessage.split()
        seqNum = int(parts[1])
        sendTime = float(parts[2])

        # Check if packets are lost
        if sequenceNumber != -1 and seqNum > sequenceNumber + 1:
            lostPackets = seqNum - sequenceNumber - 1
            print(f"Lost {lostPackets} packets")

        sequenceNumber = seqNum

        # Calculate the RTT
        rtt = recvTime - sendTime
        print(f"Received heartbeat {seqNum}, RTT: {rtt:.6f} s")

        # Acknowledge the message
        ackMessage = f"ACK {seqNum}"
        serverSocket.sendto(ackMessage.encode(), address)
    except timeout:
        continue
