import datetime
import time
from socket import *

server_name = "localhost"
server_port = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1.0)                # Sets a maximum time the socket will wait for receiving data

for seq in range(1, 11):
    try:
        msg = f"Ping {seq} at {time.ctime()}"
        start_time = time.time()
        clientSocket.sendto(msg.encode(), (server_name, server_port))

        response, _ = clientSocket.recvfrom(2048)
        end_time = time.time()

        rtt = end_time - start_time

        print(f'Response from server: {response.decode()}')
        print(f'RTT = {rtt:.6f} seconds\n')
    except timeout:
        print(f'Ping {seq}: Request timed out\n')

clientSocket.close()