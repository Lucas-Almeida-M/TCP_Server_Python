import socket
import threading
import time

class TCPServer:
    def __init__(self):
        self.IP = "192.168.0.100"
        self.PORT = 5050
        self.ADDR = (self.IP, self.PORT)
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.DISCONECT_MSG = 'DISCONECT'
        self.MESSAGE_END = "!"
        self.activeClients = 0
        self.clientsIPs = []
        self.clientDataBuffer = {}

    def handle_clients(self, conn, addr, GUI):
        print(f"New connection: {addr} connected")
        self.clientDataBuffer[addr] = [[0]*64,[0]*64,[0]*64]
        count = 0
        decodedMessage = []
        connected = True
        while connected:
            msg = str(conn.recv(self.HEADER).decode(self.FORMAT))
            if self.MESSAGE_END in msg:
                if msg[1:-1] == self.DISCONECT_MSG:
                    connected = False
                    print('Disconectando')
                    self.activeClients -= 1
                    if addr[0] in self.clientsIPs:
                        self.clientsIPs.remove(addr)
                    print(f'[{addr} : {msg}]')
                    print(f'Clients: {self.activeClients}')
                    del self.clientDataBuffer[addr]
                    break


                decodedMessage = self.decode_message(msg)
                self.clientDataBuffer[addr][0] = [decodedMessage[0]] + self.clientDataBuffer[addr][0][:-1]
                self.clientDataBuffer[addr][1] = [decodedMessage[1]] + self.clientDataBuffer[addr][1][:-1]
                self.clientDataBuffer[addr][2] = [decodedMessage[2]] + self.clientDataBuffer[addr][2][:-1]
                
                
                
                print(self.clientDataBuffer[addr][0])
                print(self.clientDataBuffer[addr][1])
                print(self.clientDataBuffer[addr][2])
                print(f'[{addr} : {msg}]')
        conn.close()

    def handle_connections(self, GUI):
        self.tcpserver.listen()
        print(f"Server is listening [{self.IP}]")
        while True:
            con, addr = self.tcpserver.accept()
            self.clientsIPs.append(addr[0])
            thread = threading.Thread(target=self.handle_clients, args=(con, addr[0], GUI))
            thread.start()
            self.activeClients = threading.active_count() - 2
            print(f'Clients: {self.activeClients}')

    def start(self, ip, port, GUI):
        self.IP = ip
        self.port = port
        self.ADDR = (self.IP, self.PORT)
        self.tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpserver.bind(self.ADDR)

        threadServer = threading.Thread(target=self.handle_connections, args=(GUI,))
        threadServer.start()


    def decode_message( self, mes):
        # device_number_start = self.encoded_message.find("$") + 1
        # device_number_end = self.encoded_message.find("$", device_number_start)
        # device_number = self.encoded_message[device_number_start:device_number_end]
        mes = str(mes)
        data_start = mes.find("$") + 1
        data_end = mes.rfind("!")
        data_part = mes[data_start:data_end]
        try:
            data_list = [int (data) for data in data_part.split("&")]
            return data_list
        except:
            return -1


        

if __name__ == "__main__":
    server = TCPServer(socket.gethostbyname(socket.gethostname()), 5050)
    server.start()


# self.tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# self.tcpserver.bind(self.ADDR)
# threadServer = threading.Thread(target=self.start())
# threadServer.start()

