import socket, sys, os, threading
DEBUG = True
# Default hostname
HOST = "localhost"
# Default FTP port*
PORT = 21

def dataCONNECTION(conn, command):
    response = ''
    print(f'dataCOnnection server invoked')
    print(f'command: {command}')
    if command.startswith('get'):
        file_name = command.split(' ')[1]
        print(f'[*] Filename: {file_name}')
        if os.path.isfile(file_name):
            conn.send('[*] OK'.encode())
            with open(file_name, 'rb') as data_file:
                conn.sendfile(data_file)
        else:
            conn.send('[*] File not found'.encode())

    elif command.startswith('put'):
        file_name = command.split(' ')[1]
        conn.send('[*] OK'.encode())
        with open(file_name, 'wb') as data_file:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data_file.write(data)

    elif command == 'ls':
        files = ' '.join(os.listdir())
        conn.send(files.encode())

    conn.close()

def controlCONNECTION(conn, addr):
    while True:
        command = conn.recv(1024).decode()
        if command == 'quit':
            break

        port = int(conn.recv(1024).decode())
        clientSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSOCKET.connect((addr[0], port))

        dataCONNECTION(clientSOCKET, command)

    conn.close()

#main function, is called at end of program
def main():
    if len(sys.argv) != 2:
        print("[*] Correct format: python + sys.argv[0] + <port number>\n")
        sys.exit(1)
    else:
        PORT = int(sys.argv[1])
        if DEBUG:
            print(f'[*] sys.argv:{sys.argv}')
            print(f'[*] PORT: {PORT}')
        # establish the socket
        clientSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSOCKET.bind((HOST, PORT))
        clientSOCKET.listen(5)
        print(f'[*] Listening to {HOST} on {PORT}')
        while True:
            conn, addr = clientSOCKET.accept()
            print(f'[+] {addr} is connected.')
            conn_thread = threading.Thread(target=controlCONNECTION, args=(conn, addr))
            conn_thread.start()
        print(f'[-] {addr} is disconnected.')


main()