from tkinter import *
from tkinter import messagebox
from tkinter import ttk
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

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Your cleanup or termination logic here
        # This function will be called when the window is closed
        print("Program closed")
        self.root.destroy()
        exit(2)
        



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
            try:
                self.tcp.start(ip, port)
                self.conn = ConnGUI(self.root, self.tcp)
            except:
                pass


class ConnGUI():
    def __init__(self, root, tcp) :
        self.root = root
        self.tcp = tcp
        self.frame = LabelFrame(root, text="Connection Manager",
                            padx=5, pady=5, bg="white", width=60)
        self.drop_bds_label = Label(
            self.frame, text="Board Select: ", bg="white", width=15, anchor="w")
        self.BoardSelectionMenu()
        # self.sync_status = Label(
        #     self.frame, text="..Sync..", bg="white", fg="orange", width=5)
        
        self.ch_label = Label(    
            self.frame, text="Active channels: ", bg="white", width=15, anchor="w")
        self.ch_status = Label(
            self.frame, text="...", bg="white", fg="orange", width=5)

        self.btn_start_stream = Button(self.frame, text="Start", state="disabled",
                                    width=5, command=self.start_stream)

        self.btn_stop_stream = Button(self.frame, text="Stop", state="disabled",
                                    width=5, command=self.stop_stream)

        self.btn_add_chart = Button(self.frame, text="+", state="disabled",
                                    width=5, bg="white", fg="#098577",
                                    command=self.new_chart)

        self.btn_kill_chart = Button(self.frame, text="-", state="disabled",
                                    width=5, bg="white", fg="#CC252C",
                                    command=self.kill_chart)
        self.save = False
        self.SaveVar = IntVar()

        self.save_check = Checkbutton(self.frame, text="Save data", variable=self.SaveVar,
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=self.save_data)

        self.separator = ttk.Separator(self.frame, orient='vertical')
        
        self.save = False
        self.SaveVar = IntVar()
        self.save_check = Checkbutton(self.frame, text="Save data", variable=self.SaveVar,
                                      onvalue=1, offvalue=0, bg="white", state="disabled",
                                      command=self.save_data)

        self.separator = ttk.Separator(self.frame, orient='vertical')

        # Optional Graphic parameters
        self.padx = 20
        self.pady = 15

        # Extending the GUI
        self.ConnGUIOpen()


    def ConnGUIOpen(self):
        '''
        Method to display all the widgets 
        '''
        self.root.geometry("1080x720")
        self.frame.grid(row=0, column=4, rowspan=3,
                        columnspan=5, padx=5, pady=5)

        self.drop_bds_label.grid(column=1, row=1)
        self.drop_bds.grid(column=2, row=1)

        self.ch_label.grid(column=1, row=2)
        self.ch_status.grid(column=2, row=2, pady=self.pady)

        self.btn_start_stream.grid(column=3, row=1, padx=self.padx)
        self.btn_stop_stream.grid(column=3, row=2, padx=self.padx)

        self.btn_add_chart.grid(column=4, row=1, padx=self.padx)
        self.btn_kill_chart.grid(column=5, row=1, padx=self.padx)

        self.save_check.grid(column=4, row=2, columnspan=2)
        self.separator.place(relx=0.65, rely=0, relwidth=0.001, relheight=1)

    def BoardSelectionMenu(self):
        self.clicked_bds = StringVar()
        bds = ["Board 1",
            "Board 2",
            "Board 3",
            "Board 4",
            "Board 5",
            "Board 6",
            "Board 8",
            "Board 9",
            "Board 9",
            "Board 10",]
        self.clicked_bds.set(bds[0])
        self.drop_bds = OptionMenu(
            self.frame, self.clicked_bds, *bds, command=self.BoardSelectionAdjust)
        self.drop_bds.config(width=10)


    def BoardSelectionAdjust(self, widget):
        self.board = self.clicked_bds.get()
        print (f"Board selected {self.board}")




    def ConnGUIClose(self):
        '''
        Method to close the connection GUI and destorys the widgets
        '''
        # Must destroy all the element so they are not kept in Memory
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        self.root.geometry("360x120")

    def start_stream(self):
        pass

    def stop_stream(self):
        pass

    def new_chart(self):
        pass

    def kill_chart(self):
        pass

    def save_data(self):
        pass

if __name__ == "__main__":
    RootGUI()
    ComGUI()
    ConnGUI()



