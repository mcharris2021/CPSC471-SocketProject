import socket, sys, os

# Default IP address
HOST = "local host"
# Default FTP port number
PORT = 21

# Recieve Hostname and Port number from user when
# executing the script
if len(sys.argv) < 2:
    print("Correct format: python " + sys.argv[0] + " <server hostname> <server port>\n")
else:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.connect((HOST, PORT))
        c.sendall(b"Hello world")
        data = c.recv(1024)

    print(f"Received {data!r}")
    c.close()
