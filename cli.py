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
        controlCONN(HOST, PORT)

#Control connection function
def controlCONN(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"[+] Connecting to {HOST}:{PORT}")
        s.connect((HOST, PORT))
        print("[+] Connected.")
        # Data connection is currently bugged
        #dataCONN(HOST, s)
        uploadFile(s)

#Data Connection Function
def dataCONN(HOST, s):
    dport = s.recv(4096).decode()
    dport = int(dport)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d:
        print(f"[+] Establishing data connection to {HOST}:{dport}")
        d.connect((HOST, dport))
        print("[+] Connected.")
        uploadFile(d)

#Test function to test transfering file to server
#creating the download function should be more or less the same as uploading,
#just reverse the client and server versions of the functions for upload (I assume)
def uploadFile(d):
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    #name of local text file on my computer, this is just for test purposes.
    #for the end product, the user would specify the name of the file to transfer
    fileName = "test1.txt"
    fileSize = os.path.getsize(fileName)
    d.send(f"{fileName}{SEPARATOR}{fileSize}".encode())
    fs = 0
    with open(fileName, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            fsTemp = sys.getsizeof(bytes_read)
            fs += fsTemp
            if not bytes_read:
                break
            d.sendall(bytes_read)

    print("Sent", fs, "bytes.")

main()
