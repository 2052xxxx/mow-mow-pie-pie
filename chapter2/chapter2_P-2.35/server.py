import socket
import threading

clients = set()
clients_lock = threading.Lock()
class ThreadedServer():
    def __init__(self, host, port):
        # global clients
        # global clients_lock
        self._host = host
        self._port = port
        self._clients = {}
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self._host, self._port))

    def listen(self):
        self._sock.listen(5)
        print("server's listening...")
        while True:
            conn, address = self._sock.accept()
            threading.Thread(target=self.listenToClient,
                             args=(conn, address)).start()
            with clients_lock:
                clients.add(conn)
            print(f"connected by {address[0]}:{address[1]}")

    def sendAll(self, conn, message):
        with clients_lock:
            for c in clients:
                if c != conn:
                    c.sendall(message.encode('utf-8'))
    
    def privateChat(self, conn, c, message):
        # while True:
        with clients_lock:
            for c in clients:
                to_c = conn.recv(1024).decode('utf-8')
                to_conn = c.recv(1024).decode('utf-8')
                if to_c is True and to_c != 'out':
                    c.send(f"[From {conn.getpeername()[1]}]{to_c}".encode('utf-8'))
                elif to_conn is True and to_conn != 'out':
                    conn.send(f"[From {c.getpeername()[1]}]{to_conn}".encode('utf-8'))


    def listenToClient(self, conn, address):
        # threading.current_thread().ident - ko có xóaaaaaa
        conn.send(str.encode('Welcome to the Server!'))
        try:
            while True:
                data = conn.recv(1024)
                if not data or data.decode('utf-8')=='bye':
                    if conn not in self._clients:
                        # message = f"port {address[1]} has left the chat"
                        message = f"{conn.getpeername()[1]} has left the chat"
                        print(message)
                    else:
                        message = f"{self._clients[conn]} has left the chat"
                        print(message)
                        del self._clients[conn]
                    self.sendAll(conn, message)
                    with clients_lock:
                        clients.remove(conn)
                    break

                if data.decode('utf-8')=='mode':
                    print(f"client {conn} request for private connection")
                    key = int(conn.recv(1024).decode("utf-8"))
                    print('output moew moew: ', key, type(key))
                    with clients_lock:
                        for c in clients:
                            if c.getpeername()[1] == key:
                                conn.send(f"Successfully connect to port {c.getpeername()[1]}".encode('utf-8'))
                                pr_mess = conn.recv(1024).decode("utf-8")
                                c.send(f"Port {conn.getpeername()[1]} have a message: {pr_mess}".encode('utf-8'))
                                # self.privateChat(conn, c, message)
                                break

                if data.decode('utf-8').lower().split()[0] == 'name':
                    name = ' '.join(data.decode('utf-8').split()[1:])
                    self._clients[conn] = name
                
                if conn not in self._clients:
                    message = f"port {address[1]}: {data.decode('utf-8')}"
                else:
                    message = f"'{self._clients[conn]}': {data.decode('utf-8')}"
                print(message )
                self.sendAll(conn, message)
                
        except socket.error:
            if conn not in self._clients:
                message = f"port {address[1]} has left the chat"
                print(message)
            else:
                message = f"{self._clients[conn]} has left the chat"
                print(message)
                del self._clients[conn]
            self.sendAll(conn, message)
            with clients_lock:
                clients.remove(conn)
        conn.close()
        
if __name__ == "__main__":
    ThreadedServer('127.0.0.1', 9999).listen()

