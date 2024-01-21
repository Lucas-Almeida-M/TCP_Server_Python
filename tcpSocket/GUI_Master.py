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
    
    def __init__(self, root, tcp):
        # Initializing the Widgets
        self.root = root
        self.tcp = tcp
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

        self.IPselect.insert(0,"192.168.0.100")
        self.Portselect.insert(0,"5050")

    def tcp_connect(self):
        ip = self.IPselect.get()
        port = int (self.Portselect.get())
        if is_valid_ip_format(ip) and (( port > 0) and (port< 65535 )):
            print(f"TRYING TO CONNECT TO SERVER  IP {ip} port {port}")
            self.tcp.start(ip, port)


if __name__ == "__main__":
    RootGUI()
    ComGUI()



