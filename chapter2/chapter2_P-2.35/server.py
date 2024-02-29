import socket
import threading

class ThreadedServer():
    def __init__(self, host, port):
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
            
            print(f"connected by {address[0]}:{address[1]}")
            # listenToClient(conn, address)

    def listenToClient(self, conn, address):
        # threading.current_thread().ident - ko có xóaaaaaa
        while True:
            conn.send(str.encode('Welcome to the Server!'))
            data = conn.recv(1024)
            if not data or data.decode('utf-8')=='bye':
                if address not in self._clients:
                    print(f"byeeeeee port {address[1]}")
                    break
                print(f"byeeeeee {self._clients[address]}")
                del self._clients[address]
                break
                # Set the response to echo back the recieved data
            if data.decode('utf-8').lower().split()[0] == 'name':
                name = ' '.join(data.decode('utf-8').split()[1:])
                self._clients[address] = name
            
            if address not in self._clients:
                message = f"port {address[1]}, {threading.current_thread().ident}: {data.decode('utf-8')}"
            else:
                message = f"name {self._clients[address]}: {data.decode('utf-8')}"
            print(message )
        conn.close()
        
def main():
    ThreadedServer('127.0.0.1', 9999).listen()

if __name__ == "__main__":
    main()
