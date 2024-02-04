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
        self.clientSyncCount  = {}
        self.clientSyncStatus = {} 


        self.MESSAGETYPE_CONFIG     = 0
        self.MESSAGETYPE_DATA       = 1
        self.MESSAGETYPE_SYNC       = 2
        self.MESSAGETYPE_DISCONNECT = 3



    def handle_clients(self, conn, addr):
        print(f"New connection: {addr} connected")
        self.clientSyncCount[addr]  =  0
        self.clientSyncStatus[addr] = [0]*10
        self.clientDataBuffer[addr] = [[0]*64,[0]*64,[0]*64,[0]*64,[0]*64,[0]*64,[0]*64,[0]*64]
        count = 0
        decodedMessage = []
        connected = True
        while connected:
            msg = str(conn.recv(self.HEADER).decode(self.FORMAT))
            print(msg)
            if self.MESSAGE_END in msg:
                self.process_message( addr, msg)
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


    def process_message( self, addr, mes):
        mes = str(mes)
        if mes[0] == "@" and mes[-1] == "!":
            match = re.search(r"@\$([^\$]*)\$&(.*)&!", mes)
            if match:
                MessageType = int(match.group(1))
                print(MessageType)
            match MessageType:
                case self.MESSAGETYPE_CONFIG:
                    
                    pass
                case self.MESSAGETYPE_DATA:
                    pass
                case self.MESSAGETYPE_SYNC:
                   
                    data = [int(s) for s in (match.group(2).split("&"))]        
                    self.clientSyncCount[addr] = data[0]
                    for i in range (10):
                        self.clientSyncStatus[addr][i] = data[i+1]
                        if i < 8: # Gambiarra, faltou dois checkbox
                            if (data[i+1]):
                                self.GUI.device_check[i]["state"] = "active" 
                            else:
                                self.GUI.device_check[i]["state"] = "disabled" 
                                self.GUI.device_check_var[i].set(data[i+1])
                        
                        #Tem que ter um if pra saber qual board ta selecionadona dropbox
                    print(data)
                    self.GUI.active_devices["text"] = str(self.clientSyncCount[addr])
                    pass
                case self.MESSAGETYPE_DISCONNECT:
                    pass
        else:
            return -1  # Error message  
        


        

if __name__ == "__main__":
    server = TCPServer(socket.gethostbyname(socket.gethostname()), 5050)
    server.start()


# self.tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# self.tcpserver.bind(self.ADDR)
# threadServer = threading.Thread(target=self.start())
# threadServer.start()

