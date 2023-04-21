import socket, sys, os

# Default IP address
HOST = "local host"
# Default FTP port number
PORT = 21

#Main function, called at the end
def main():
    if len(sys.argv) < 2:
        print("Correct format: python " + sys.argv[0] + " <server hostname> <server port>\n")
    else:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])
        # call the control connection function
        control(HOST, PORT)

#Control connection function
def control(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello world")
        data = s.recv(1024)

    print(f"Received {data!r}")
    s.close()

main()
