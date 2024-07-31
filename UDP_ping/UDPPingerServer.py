# UDPPingerServer.py 
# We will need the following module to generate randomized lost packets import random 
from socket import * 
import time
import random

# Create a UDP socket  
# Notice the use of SOCK_DGRAM for UDP packets 
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
    except timeout:
        continue     
	# Generate random number in the range of 0 to 10 
    rand = random.randint(0, 10)     

	# Capitalize the message from the client     
    message = message.upper() 
	# If rand is less is than 4, we consider the packet lost and do not respond     
    if rand < 4:         
	    continue     
	# Otherwise, the server responds         
    serverSocket.sendto(message, address) 