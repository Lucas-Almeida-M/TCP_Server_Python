import socket
import threading
import time
import re


class TCPServer:
    def __init__(self):
        self.IP = "192.168.0.100"
        self.PORT = 8000
        self.ADDR = (self.IP, self.PORT)
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.DISCONECT_MSG = 'DISCONECT'
        self.MESSAGE_END = "!"
        self.activeClients = 0
        self.clientsIPs = []
        self.clientDataBuffer = {}


        self.MESSAGETYPE_CONFIG     = 0
        self.MESSAGETYPE_DATA       = 1
        self.MESSAGETYPE_SYNC       = 2
        self.MESSAGETYPE_DISCONNECT = 3



    def handle_clients(self, conn, addr):
        print(f"New connection: {addr} connected")
        self.data.add_client(addr)
        count = 0
        decodedMessage = []
        connected = True
        while connected:
            msg = str(conn.recv(self.HEADER).decode(self.FORMAT))
            print(msg)
            if self.MESSAGE_END in msg:
                result = self.data.process_message( addr, msg)
                match result[0]:
                    case self.MESSAGETYPE_SYNC:
                        self.GUI.gui_sync_update()
                    case self.MESSAGETYPE_DATA:
                        self.GUI.update_graph(addr, result[1])
        conn.close()

    def handle_connections(self):
        self.tcpserver.listen()
        print(f"Server is listening [{self.IP}]")
        while True:
            con, addr = self.tcpserver.accept()
            self.clientsIPs.append(addr[0])
            thread = threading.Thread(target=self.handle_clients, args=(con, addr[0]))
            thread.start()
            self.activeClients = threading.active_count() - 2
            print(f'Clients: {self.activeClients}')

    def start(self, ip, port, GUI, data):
        self.data = data
        self.GUI = GUI
        self.IP = ip
        self.PORT = port
        self.ADDR = (self.IP, self.PORT)
        self.tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpserver.bind(self.ADDR)

        threadServer = threading.Thread(target=self.handle_connections)
        threadServer.start()
        

if __name__ == "__main__":
    server = TCPServer(socket.gethostbyname(socket.gethostname()), 5050)
    server.start()


# self.tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# self.tcpserver.bind(self.ADDR)
# threadServer = threading.Thread(target=self.start())
# threadServer.start()

