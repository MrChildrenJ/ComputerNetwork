from socket import *

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)          # 1: max number of queued connections
print("The sever is running at port " + str(serverPort))

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    cap_sentence = sentence.upper()
    connectionSocket.send(cap_sentence.encode())
    connectionSocket.close()