import socket
import threading
import re


class TCPServer:
    def __init__(self):
        self.IP = "192.168.0.100"
        self.PORT = 8000
        self.ADDR = (self.IP, self.PORT)
        self.HEADER = 128
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
        self.data.create_client_folder(addr)
        self.GUI.BoardSelectionMenu(str(addr))
        count = 0
        decodedMessage = []
        connected = True
        while connected:
            try:
                msg = str(conn.recv(self.HEADER).decode(self.FORMAT))
                print(msg)
                msgBuff = re.split('(?<=!)', msg)
                for i in range (len(msgBuff) - 1):
                    self.data.process_message( self.GUI, addr, msgBuff[i])
            except:
                pass
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
