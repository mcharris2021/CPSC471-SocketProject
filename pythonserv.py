import socket, sys

# Default hostname
HOST = "localhost"
# Default FTP port
PORT = 21


if len(sys.argv) < 2:
    print("Correct format: python " + sys.argv[0] + " <port number>\n")
else:
    PORT = int(sys.argv[1])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        while True:
            print("Waiting for connections...")
            conn, addr = s.accept()
            with conn:
                print("Connected by", addr[0])
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
            conn.close()
            break
