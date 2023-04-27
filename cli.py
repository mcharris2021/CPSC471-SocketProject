import socket, sys, os, random

# Default IP address
HOST = "localhost"
# Default FTP port number
PORT = 1234
DEBUG = True

def dataCONNECTION():
    dp = random.randint(1024, 65535)
    ds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ds.bind(('', dp))
    ds.listen(1)
    return ds, dp

def _get(clientSOCKET, command):
    clientSOCKET.send(command.encode())
    response = clientSOCKET.recv(1024).decode()

    if response == 'OK':
        file_name = command.split(' ')[1]
        ds, dp = dataCONNECTION()
        clientSOCKET.send(str(dp).encode())

        conn, _ = ds.accept()
        with open(file_name, 'wb') as data_file:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data_file.write(data)

        conn.close()
        ds.close()
    else:
        print(response)

def _put(clientSOCKET, command):
    filename = command.split(' ')[1]

    if os.path.isfile(filename):
        clientSOCKET.send(command.encode())
        clientSOCKET.recv(1024).decode()

        ds, dp = dataCONNECTION()
        clientSOCKET.send(str(dp).encode())

        conn, _ = ds.accept()
        with open(filename, 'rb') as data_file:
            conn.sendfile(data_file)

        conn.close()
        ds.close()
    else:
        print('File not found')

def _ls(clientSOCKET):
    clientSOCKET.send('ls'.encode())
    ds, dp = dataCONNECTION()
    clientSOCKET.send(str(dp).encode())

    conn, _ = ds.accept()
    data = conn.recv(1024).decode()
    print(data)

    conn.close()
    ds.close()

def main():
    if len(sys.argv) != 3:
        print("[*] Usage: cli.py <server machine> <server port>")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    clientSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSOCKET.connect((HOST, PORT))

    while True:
        command = input("ftp> ")

        if command.startswith('get'):
            _get(clientSOCKET, command)
        elif command.startswith('put'):
            _put(clientSOCKET, command)
        elif command == 'ls':
            _ls(clientSOCKET)
        elif command == 'quit':
            clientSOCKET.send(command.encode())
            break
        else:
            print("Invalid command")

    clientSOCKET.close()


main()
