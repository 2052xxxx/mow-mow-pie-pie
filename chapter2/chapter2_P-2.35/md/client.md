```
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    while True:
        response = client_socket.recv(1024).decode()
        print('Server says:', response)
        message = input(" -> ")
        while message.lower().strip() != 'bye':
            client_socket.send(message.encode())
            message = input(" -> ")
        break
    client_socket.close()

if __name__ == '__main__':
    client_program()
```
