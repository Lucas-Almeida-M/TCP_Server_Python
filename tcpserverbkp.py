import socket
import threading


PORT = 5050
# SERVER = "192.168.0.100"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
DISCONECT_MSG = 'DISCONECT' 
MESSAGE_END = "lf"


tcpserver = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM )
tcpserver.bind(ADDR)


def handle_clients(conn, addr):
    print(f"New connection : {addr} connected")
    connected = True
    while (connected):
        msg = str(conn.recv(HEADER).decode(FORMAT))
        if (MESSAGE_END in msg):
            message = msg.split("lf")[0]
            if (message == DISCONECT_MSG):
                connected = False
            print(f'[{addr} : {message}]')
    conn.close()
        


    pass

def start():
    tcpserver.listen()
    print(f"Server is listening [{SERVER}]")
    while (True):
        con, addr = tcpserver.accept()
        thread = threading.Thread(target=handle_clients, args=(con, addr))
        thread.start()
        print(f'Clients : {threading.active_count() - 1 }')


start()