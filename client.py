import socket

HOST = "0.0.0.0"
PORT = 6000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.sendall(b"Hello world")
    data = s.recv(1024)

print(f"Received {data!r}")
