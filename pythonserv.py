import socket, sys

# Default hostname
HOST = "localhost"
# Default FTP port
PORT = 21

def main():
    if len(sys.argv) < 2:
        print("Correct format: python " + sys.argv[0] + " <port number>\n")
    else:
        PORT = int(sys.argv[1])
        control(HOST, PORT)

def control(HOST, PORT):
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
            # This stops the server, if you want the
            # server to keep running after ending connections
            # comment out the break
            break

main()