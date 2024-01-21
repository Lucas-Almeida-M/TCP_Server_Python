from tkinter import *
import re
import socket
import threading


def is_valid_ip_format(input_string):
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

    if ip_pattern.match(input_string):
        return True
    else:
        return False



class RootGUI():
    def __init__(self):
        '''Initializing the root GUI and other comps of the program'''
        self.root = Tk()
        self.root.title("Data vizualizer")
        self.root.geometry("1080x720")
        self.root.config(bg="white")


# Classe de comunicação com o microcontrolador
class ComGUI():
    def __init__(self, root):
        #Parameetros de comunicação
        self.IP = "000.000.000.000"
        self.PORT = 65535
        self.ADDR = (self.IP, self.PORT)
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.DISCONECT_MSG = 'DISCONECT'
        self.MESSAGE_END = "lf"



        # Initializing the Widgets
        self.root = root
        self.frame = LabelFrame(root, text="Tcp Socket",
                                padx=5, pady=5, bg="white")
        self.server_ip = Label(
            self.frame, text="Server IP: ", bg="white", width=15, anchor="w")
        self.server_port = Label(
            self.frame, text="Server Port: ", bg="white", width=15, anchor="w")

        # Setup the Drop option menu
        self.ServerIPOptionMenu()
        # self.ComOptionMenu()

        # Add the control buttons for refreshing the COMs & Connect
        self.btn_connect = Button(self.frame, text="Connect",
                                  width=10, state="active",  command=self.tcp_connect)

        # Optional Graphic parameters
        self.padx = 20
        self.pady = 5

        # Put on the grid all the elements
        self.publish()

    def publish(self):
        '''
         Method to display all the Widget of the main frame
        '''
        self.frame.grid(row=0, column=0, rowspan=3,
                        columnspan=3, padx=5, pady=5)
        self.server_ip.grid(column=1, row=2)
        self.server_port.grid(column=1, row=3)

        self.IPselect.grid(column=2, row=2, padx=self.padx, pady=self.pady)
        self.Portselect.grid(column=2, row=3, padx=self.padx, pady=self.pady)
        # self.drop_com.grid(column=2, row=2, padx=self.padx)

        self.btn_connect.grid(column=3, row=2)

    def ServerIPOptionMenu(self):
        self.IPselect = Entry(self.frame, width=30)
        self.Portselect = Entry(self.frame, width=30)

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

    def ServerStart(self):
        self.tcpserver.listen()
        print(f"Server is listening [{self.server_ip}]")
        while True:
            con, addr = self.tcpserver.accept()
            thread = threading.Thread(target=self.handle_clients, args=(con, addr))
            thread.start()
            print(f'Clients: {threading.active_count() - 2}')


    def tcp_connect(self):
        if is_valid_ip_format(self.IPselect.get()) and ( (int( self.Portselect.get()) > 0) and (int(self.Portselect.get())< 65535 )):

            self.IP = str(self.IPselect.get())
            self.PORT = int(self.Portselect.get())
            self.ADDR = (self.IP, self.PORT)
            print(self.ADDR)
            self.tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcpserver.bind(self.ADDR)
            threadTCP = threading.Thread(target=self.ServerStart)
            threadTCP.start()


if __name__ == "__main__":
    RootGUI()
    ComGUI()



