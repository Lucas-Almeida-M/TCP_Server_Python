import socket
import threading

class TCPServer:
    def __init__(self):
        self.IP = "192.168.0.100"
        self.PORT = 5050
        self.ADDR = (self.IP, self.PORT)
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.DISCONECT_MSG = 'DISCONECT'
        self.MESSAGE_END = "lf"
        self.activeClients = 0

    def handle_clients(self, conn, addr):
        print(f"New connection: {addr} connected")
        connected = True
        while connected:
            msg = str(conn.recv(self.HEADER).decode(self.FORMAT))
            if self.MESSAGE_END in msg:
                message = msg.split(self.MESSAGE_END)[0]
                if message == self.DISCONECT_MSG:
                    connected = False
                    print('Disconectando')
                    self.activeClients -= 1
                    print(f'[{addr} : {message}]')
                    print(f'Clients: {self.activeClients}')
                    break
                print(f'[{addr} : {message}]')
        conn.close()

    def handle_connections(self):
        self.tcpserver.listen()
        print(f"Server is listening [{self.IP}]")
        while True:
            con, addr = self.tcpserver.accept()
            thread = threading.Thread(target=self.handle_clients, args=(con, addr))
            thread.start()
            self.activeClients = threading.active_count() - 2
            print(f'Clients: {self.activeClients}')

    def start(self, ip, port):
        self.IP = ip
        self.port = port
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

