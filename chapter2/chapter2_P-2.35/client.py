import threading
import sys
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 9999  # The port used by the server

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()
        while True:
            try:
                message = input()
                while message.lower().strip() != 'bye':
                    client_socket.send(message.encode('utf-8'))
                    if message.lower().strip() != 'mode':
                        message = input()
                    elif message.lower().strip() == 'mode':
                        key = input("Input port: ")
                        client_socket.send(key.encode('utf-8'))
                        message = input("[PPPPPP]: ")
                        # client_socket.send(pr_mess.encode('utf-8'))

                        # yield

                    #     response = client_socket.recv(1024).decode('utf-8')
                    #     if response == f"Successfully connect to port {message}":
                    #         privateChat(client_socket)
                # client_socket.send(message.encode('utf-8'))
                break
            except:
                print("Closed the connection.")
                break
        client_socket.close()
        receive_thread.join()
    except ConnectionRefusedError:
        print("server didn't even exist :v")
        client_socket.close()

def receive_messages(client_socket):
    while True:
        try:
            response = client_socket.recv(1024).decode('utf-8')
            print(response)
        except:
            print("Connection to the server closed.")
            break

# def privateChat(client_socket):
#     receive_thread = threading.Thread()
#     receive_thread.start()
#     while True:
#         try:
#             message = input()
#             while message.lower().strip() != 'out':
#                 client_socket.send(message.encode('utf-8'))
#                 message = input()
#             client_socket.send(message.encode('utf-8'))
#             break
#         except:
#             print("Closed private chat.")
#             break
#     client_socket.close()
#     receive_thread.join()
        
if __name__ == '__main__':
    client_program()