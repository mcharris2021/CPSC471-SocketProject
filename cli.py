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
        print(f"[+] Connecting to {HOST}:{PORT}")
        s.connect((HOST, PORT))
        print("[+] Connected.")
        uploadFile(s)
    s.close()

#Test function to test transfering file to server
def uploadFile(s):
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    #name of local text file on my computer
    fileName = "test1.txt"
    fileSize = os.path.getsize(fileName)
    s.send(f"{fileName}{SEPARATOR}{fileSize}".encode())
    
    with open(fileName, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)

    print("Sent", fileSize, "bytes.")

main()
