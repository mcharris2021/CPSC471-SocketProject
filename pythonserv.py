import socket, sys, os

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
            print(f"[*] Listening as {HOST}:{PORT}")
            conn, addr = s.accept()
            with conn:
                print(f"[+] {addr} is connected.")
                fileTest(conn)
            conn.close()
            print(f"[-] {addr} is disconnected.")
            break

#Test function to test receiving file from client
def fileTest(conn):
	BUFFER_SIZE = 4096
	SEPARATOR = "<SEPARATOR>"
	rcvTemp = conn.recv(BUFFER_SIZE).decode()
	filename, filesize = rcvTemp.split(SEPARATOR)
	filename = os.path.basename(filename)
	with open(filename, "wb") as f:
		while True:
			bytes_read = conn.recv(BUFFER_SIZE)
			if not bytes_read:
				break
			f.write(bytes_read)
	print(f"[+] File {filename} received")
main()