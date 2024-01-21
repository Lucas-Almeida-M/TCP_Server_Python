import socket
import threading

class TCPServer:
    def __init__(self, host, port):
        self.SERVER = host
        self.PORT = port
        self.ADDR = (self.SERVER, self.PORT)
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.DISCONECT_MSG = 'DISCONECT'
        self.MESSAGE_END = "lf"

        self.tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpserver.bind(self.ADDR)

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
                print(f'[{addr} : {message}]')
        conn.close()

    def start(self):
        self.tcpserver.listen()
        print(f"Server is listening [{self.SERVER}]")
        while True:
            con, addr = self.tcpserver.accept()
            thread = threading.Thread(target=self.handle_clients, args=(con, addr))
            thread.start()
            print(f'Clients: {threading.active_count() - 1}')

if __name__ == "__main__":
    server = TCPServer(socket.gethostbyname(socket.gethostname()), 5050)
    server.start()

