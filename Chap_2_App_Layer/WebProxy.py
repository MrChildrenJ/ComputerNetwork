from socket import *
import sys

server_port = 8888

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind(('', server_port))
tcpSerSock.listen(5)

try:
    while True:
        print(f"Web proxy server is running on port: {server_port}")
        tcpCliSock, addr = tcpSerSock.accept()
        print('Received a connection from:', addr)              # http://localhost:8888/www.google.com

        message = tcpCliSock.recv(2048).decode()
        print(f"message = {message}")                           # GET /www.google.com HTTP/1.1

        # Extract the filename from the given message
        print(f"message.split()[1] = {message.split()[1]}")     # /www.google.com
        filename = message.split()[1].partition("/")[2]
        print(f"filename = {filename}")                         # www.google.com

        fileExist = "false"
        filetouse = "/" + filename
        print(f"filetouse = {filetouse}")                       # /www.google.com

        try:
            # Check whether the file exist in the cache
            f = open(filetouse[1:], "r")    # r: open for reading
            outputdata = f.readlines()      # outputdata is a LIST!!
            fileExist = "true"

            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
            tcpCliSock.send("Content-Type:text/html\r\n".encode())

            for line in outputdata:
                tcpCliSock.send(line.encode())

            print('Read from cache')

        # Error handling for file not found in cache
        except IOError:
            if fileExist == "false":
                # Create a socket on the proxy server
                c = socket(AF_INET, SOCK_STREAM)

                hostn = filename.replace("www.","",1)
                print(f"hostn is {hostn}")

                try:
                    # Create a temporary file on this socket and ask port 80 for the file requested by the client
                    c.connect((hostn, 80))
                    request = f"GET https://{filename} HTTP/1.0\r\nHost: {hostn}\r\n\r\n"
                    c.send(request.encode())

                    # Read the response into buffer
                    buff = c.recv(2048)

                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket and the corresponding file in the cache
                    tmpFile = open("./" + filename,"wb")

                    tmpFile.write(buff)

                    tcpCliSock.send(buff)

                except Exception as e:
                    print(f"Illegal request: {str(e)}")
                    tcpCliSock.send("HTTP/1.1 500 Internal Server Error\r\n\r\n".encode())
                    tcpCliSock.send("<html><body><h1>500 Internal Server Error</h1></body></html>\r\n".encode())

                finally:
                    c.close()
            else:
                # HTTP response message for file not found
                tcpCliSock.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                tcpCliSock.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

        # Close the client and the server sockets
        tcpCliSock.close()

except KeyboardInterrupt:
    print("\nShutting down the proxy server.")

finally:
    tcpSerSock.close()