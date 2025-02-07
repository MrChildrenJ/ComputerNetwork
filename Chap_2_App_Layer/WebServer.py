import sys
from socket import *
import threading

serverPort = 12000

def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()      # ex: GET /somedir/page.html HTTP/1.1
        filename = message.split()[1]                       # filename[1] = /somedir/page.html
                                                            # filename[0] is method: GET, POST, HEAD, PUT, DELETE
        f = open(filename[1:], 'rb')                        # rb: open in binary mode
        # Adding 'rb' is best practice
        # Because we need to handle both text files (like .html, .js, .css) AND binary files (like images, .pdf, etc.)
        # Default is text mode, which will using UTF-8

        outputdata = f.read()

        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())   # Send one HTTP header line into socket
        connectionSocket.send(outputdata)
    except IOError:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
    finally:
        connectionSocket.close()


serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# Without this line: When we stop server, the OS keeps that port in "TIME_WAIT" state for a while
# SOL_SOCKET - indicates we're setting a socket-level option (SOL: Socket Option Level)
# SO_REUSEADDR - the specific option that allows address reuse
# 1 - turns this option ON (0 would turn it OFF)

serverSocket.bind(('', serverPort))     # '' = 0.0.0.0 = Listen on ALL available network interfaces

# Listen only on localhost
# serverSocket.bind(('127.0.0.1', 12000))

# Listen on a specific network interface
# serverSocket.bind(('192.168.1.100', 12000))

serverSocket.listen(5)

try:
    while True:
        print('Ready to serve at port: ' + str(serverPort))
        connectionSocket, addr = serverSocket.accept()

        #client_thread = threading.Thread(target=handle_client(connectionSocket)) -> WRONG!!!
        #It will EXECUTE the function immediately in the main thread, and try to use the RESULT of that function as the target

        client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
        # Correct. Because:
        # 1. target expects a function reference (not a function call)
        # 2. args is where you pass the arguments that will be used when the function is called in the new thread

        client_thread.start()
except KeyboardInterrupt:
    print("\nShutting down server gracefully...")
    serverSocket.close()
    sys.exit()