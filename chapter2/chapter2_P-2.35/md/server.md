```
import socket
import time
from _thread import *

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 9999  # Port to listen on (non-privileged ports are > 1023)
ThreadCount = 0

def threaded_client(connection, addr):
    connection.send(str.encode('Welcome to the Server!'))
    while True:
        data = connection.recv(2048)
        # reply = 'Server Says: ' + data.decode('utf-8')
        if not data or data.decode()=='bye':
            break
        print(f"from user port {addr[1]}, fileno({connection.fileno()}): {data.decode()}" )
    print(f"byeeeeee port {addr[1]}")
    connection.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    try:
        server.bind((HOST, PORT))
    except socket.error as e:
        print(str(e))
    server.listen()
    print("server's listening...")
    while True:
        conn, addr = server.accept()
        print(f"connected by {addr[0]}:{addr[1]}")
        a = start_new_thread(threaded_client, (conn, addr))
        ThreadCount += 1
        print(f'Thread Number: {str(ThreadCount)}, port: {addr[1]}, thredid: {a}' )

```

```
from socket import *
from codecs import decode
#from chatrecord import ChatRecord
from threading import Thread
from time import ctime

class ClientHandler(Thread):

    def __init__(self, conn,address):
        global sockets
        global addresses
        Thread.__init__(self)
        self._conn = conn
        self._address = address
        sockets.append(self._conn)
        addresses.append(self._address)

    def run(self):
        self._conn.send('Welcome to the chatroom!\n')

        while 1:
            message =self._conn.recv(BUFSIZE)
            print '\n\n',sockets
            if not message:
                print "Client disconnected."
                addIndex=sockets.index(self._conn)
                del sockets[addIndex]
                del addresses[addIndex]
                self._conn.close()
                break
            else:
                if 'ONLINE#' in message:
                    for x in sockets:
                        if (x!=self._conn):
                            try:
                                x.send(message[7:])
                            except:
                                print 'disconnected'
                                continue
                    print message[7:]
                else:
                    for x in sockets:
                        try:
                            x.send(message)
                            /*sockets is the list of all client*/
                        except:
                            print ' '
                            continue
                    print message


HOST = 'localhost'
PORT = 1235
ADDRESS = (HOST,PORT)
BUFSIZE = 1024
server = socket(AF_INET,SOCK_STREAM)
server.bind(ADDRESS)
server.listen(5)
sockets=[]
addresses=[]

while True:
    print "Waiting for connection..."
    conn, address = server.accept()
    print('...client connected from: ',address)
    handler = ClientHandler(conn, address)
    handler.start()
```
