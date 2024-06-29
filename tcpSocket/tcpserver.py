import socket
import threading
import re
import time


class TCPServer:
    def __init__(self):
        self.IP = "192.168.0.100"
        self.PORT = 8000
        self.ADDR = (self.IP, self.PORT)
        self.HEADER = 128
        self.FORMAT = 'utf-8'
        self.DISCONECT_MSG = 'DISCONECT'
        self.MESSAGE_END = "!"
        self.connected = False
        self.activeClients = 0
        self.clientsIPs = []
        self.clientDataBuffer = {}
        self.conn_reg = {}
        self.handle_connections_thread = 0
        self.handle_clients_thread = []


    def handle_clients(self, conn, addr):
        print(f"New connection: {addr} connected")
        self.data.add_client(addr)
        self.data.create_client_folder(addr)
        self.GUI.BoardSelectionMenu(str(addr))
        self.conn_reg[str(addr)] = conn
        count = 0
        decodedMessage = []
        self.connected = True
        while self.connected:
            try:
                msg = str(conn.recv(self.HEADER).decode(self.FORMAT))
                print(msg)
                msgBuff = re.split('(?<=!)', msg)
                for i in range (len(msgBuff) - 1):
                    self.data.process_message( self.GUI, addr, msgBuff[i])
            except Exception as e:
                print(f"Error: {e}")
        conn.close()

    def handle_connections(self):
        self.tcpserver.listen()
        print(f"Server is listening [{self.IP}]")
        while self.started:
            try:
                conn, addr = self.tcpserver.accept()
                self.clientsIPs.append(addr[0])
                thread = threading.Thread(target=self.handle_clients, args=(conn, addr[0]))
                thread.start()
                self.activeClients = threading.active_count() - 2
                print(f'Clients: {self.activeClients}')

            except socket.timeout:
                continue
            except Exception as e:
                print(f"Exception in accept: {e}")    

    def start(self, ip, port, GUI, data):
        self.data = data
        self.GUI = GUI
        self.IP = ip
        self.PORT = port
        self.ADDR = (self.IP, self.PORT)
        self.tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpserver.bind(self.ADDR)
        self.started = True
        self.handle_connections_thread = threading.Thread(target=self.handle_connections)
        self.handle_connections_thread.start()

    def stop(self):
        self.connected = False
        self.started = False
        time.sleep(0.2)
        self.tcpserver.close()
        

    def send_message(self, msg, addr):
        self.conn_reg[str(addr)].send(msg.encode('utf-8'))
        

if __name__ == "__main__":
    server = TCPServer(socket.gethostbyname(socket.gethostname()), 5050)
    server.start()
