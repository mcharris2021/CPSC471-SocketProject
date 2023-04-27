import socket, sys, os

# Default IP address
HOST = "local host"
# Default FTP port number
PORT = 21

#Main function, called at the end
def main():
    if len(sys.argv) < 2:
        print("[*] Correct format: python " + sys.argv[0] + " <server hostname> <server port>\n")
    else:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])
        # call the control connection function
        controlCONN(HOST, PORT)
       

#Control connection function
def controlCONN(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"[*] Connecting to {HOST}:{PORT}")
        s.connect((HOST, PORT))
        print("[+] Connected.")

        command = display_menu(HOST,PORT) 

        s.send(command.encode())
        # Receive the response from the server
        response = s.recv(1024).decode()
        print(f'response:{response}')
        # Parse FTP response and execute it
        if response.startswith("get "):
            filename = response.split()[1]
            with open(filename, "wb") as f:
                data = s.recv(1024)
                while data:
                    f.write(data)
                    data = s.recv(1024)
            print("File downloaded: " + filename)
        elif response.startswith("put "):
           # print(f'put command reached') TESTING
            filename = response.split()[1]
            
            with open(filename, "rb") as f:
                data = f.read(1024)
                while data:
                    s.send(data)
                    data = f.read(1024)
            print("File uploaded: " + filename)
        elif response == "ls":
            data = s.recv(1024)
            while data:
                print(data.decode(), end="")
                data = s.recv(1024)
        elif response == "quit":
            s.close()
            return 0
        else:
            print("Testing else")

        # Data connection is currently bugged
        #dataCONN(HOST, s)

        uploadFile(s)
    print(f"[-] Disconnected from {HOST}:{PORT}")
 
def display_menu(HOST,PORT):
        
    # Display menu options
    print("Enter one of the following command prompts:")
    print("ftp> get <file name> (downloads file <file name> from the server)") 
    print("ftp> put <filename> (uploads file <file name> to the server)")
    print("ftp> ls(lists files on the server)")
    print("ftp> quit (disconnects from the server and exits)")

   #while True:

    # Prompt user for FTP command
    command = input("ftp> ")

    # Send the FTP command to the server
    print(f'command:{command}')
    #print(f's:{s}')

    return command


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
    print("[DEBUG] Sent", fs, "bytes.")

main()
