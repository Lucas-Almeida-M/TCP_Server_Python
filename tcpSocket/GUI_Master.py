import os
import signal
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import re
import socket
import threading

import matplotlib.pyplot as plt  # pip install matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)




class RootGUI():
    def __init__(self):
        '''Initializing the root GUI and other comps of the program'''
        self.root = Tk()
        self.root.title("Data vizualizer")
        self.root.geometry("1920x1080")
        self.root.config(bg="white")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Your cleanup or termination logic here
        # This function will be called when the window is closed
        print("Program closed")
        os.kill(os.getpid(), signal.SIGTERM)
        self.root.destroy()
        exit(2)
        
# Classe de comunicação com o microcontrolador
class ComGUI():
    
    def __init__(self, root, tcp, data):
        # Initializing the Widgets
        self.root = root
        self.tcp = tcp
        self.data = data
        self.frame = LabelFrame(root, text="Tcp Socket",
                                padx=5, pady=5, bg="yellow")
        self.server_ip = Label(
            self.frame, text="Server IP: ", bg="white", width=15, anchor="w")
        self.server_port = Label(
            self.frame, text="Server Port: ", bg="white", width=15, anchor="w")

        # Setup the Drop option menu
        self.ServerIPOptionMenu()
        # self.ComOptionMenu()

        # Add the control buttons for refreshing the COMs & Connect
        self.btn_connect = Button(self.frame, text="Start Server",
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
        self.Portselect.insert(0,"8000")

    def tcp_connect(self):
        ip = self.IPselect.get()
        port = int (self.Portselect.get())
        if self.is_valid_ip_format(ip) and (( port > 0) and (port< 65535 )):
            print(f"TRYING TO CONNECT TO SERVER  IP {ip} port {port}")
            try:
                self.conn = ConnGUI(self.root, self.tcp, self.data)
                self.btn_connect["text"] = "Started"
                self.btn_connect["state"] = "disabled"

                self.tcp.start(ip, port, self.conn, self.data)
                
            except:
                pass

    def is_valid_ip_format(self,input_string):
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

        if ip_pattern.match(input_string):
            return True
        else:
            return False



        


class ConnGUI():
    def __init__(self, root, tcp, data) :
        self.root = root
        self.tcp = tcp
        self.data = data
        self.frame = LabelFrame(root, text="Connection Manager",
                            padx=5, pady=5, bg="green", width=60)
        self.drop_bds_label = Label(
            self.frame, text="Board Select: ", bg="white", width=15, anchor="w")
        self.BoardSelectionMenu()
        # self.sync_status = Label(
        #     self.frame, text="..Sync..", bg="white", fg="orange", width=5)
        
        self.active_devices_label = Label(    
            self.frame, text="Active Devices: ", bg="white", width=15, anchor="w")
        self.active_devices = Label(
            self.frame, text="0", bg="white", fg="orange", width=5)

        # self.btn_add_chart = Button(self.frame, text="+", state="active",
        #                             width=5, bg="white", fg="#098577",
        #                             command=self.new_chart)

        # self.btn_kill_chart = Button(self.frame, text="-", state="active",
        #                             width=5, bg="white", fg="#CC252C",
        #                             command=self.kill_chart)

        self.device_check_var = []
        self.device_check = []

        self.device_check_var.append(IntVar())
       
        self.device_check.append( Checkbutton(self.frame, text="Device 0", variable=self.device_check_var[0],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=self.display_graphs))
        
        self.device_check_var.append(IntVar())
        self.device_check.append( Checkbutton(self.frame, text="Device 1", variable=self.device_check_var[1],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=self.display_graphs) )
        
        self.device_check_var.append(IntVar())
        self.device_check.append( Checkbutton(self.frame, text="Device 2", variable=self.device_check_var[2],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=self.display_graphs))
        
        self.device_check_var.append(IntVar())
        self.device_check.append(Checkbutton(self.frame, text="Device 3", variable=self.device_check_var[3],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=self.display_graphs))
        
        self.device_check_var.append(IntVar())
        self.device_check.append(Checkbutton(self.frame, text="Device 4", variable=self.device_check_var[4],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=self.display_graphs))
        
        self.device_check_var.append(IntVar())
        self.device_check.append( Checkbutton(self.frame, text="Device 5", variable=self.device_check_var[5],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=self.display_graphs))
        
        self.device_check_var.append(IntVar())
        self.device_check.append( Checkbutton(self.frame, text="Device 6", variable=self.device_check_var[6],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=self.display_graphs))
        
        self.device_check_var.append(IntVar())
        self.device_check.append( Checkbutton(self.frame, text="Device 7", variable=self.device_check_var[7],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=self.display_graphs))
        


        self.btn_start_stream = Button(self.frame, text="Start", state="active",
                                    width=5, command=self.display_graphs)

        self.btn_stop_stream = Button(self.frame, text="Stop", state="disabled",
                                    width=5, command=self.stop_stream)
        self.save = False
        self.SaveVar = IntVar()

        self.save_check = Checkbutton(self.frame, text="Save data", variable=self.SaveVar,
                                    onvalue=1, offvalue=0, bg="white", state="active",
                                    command=self.save_data)

        self.separator = ttk.Separator(self.frame, orient='vertical')
        self.separator2 = ttk.Separator(self.frame, orient='vertical')
        
        # Optional Graphic parameters
        self.padx = (40,5)
        self.pady = (40,5)

        # Extending the GUI
        self.ConnGUIOpen()
        self.chartMaster = displayGUI(self.root, self.tcp, self.data)

    def display_graphs(self):
        

        self.chartMaster.AddChannelMaster()

        pass
        
    def ConnGUIOpen(self):
        '''
        Method to display all the widgets 
        '''
        # self.root.geometry("1080x720")
        self.frame.grid(row=0, column=3, rowspan=3,
                        columnspan=18, padx=5, pady=5, sticky='nsew')

        self.drop_bds_label.grid(column=1, row=1)
        self.drop_bds.grid(column=2, row=1, padx=(0, 40))

        self.active_devices_label.grid(column=1, row=2)
        self.active_devices.grid(column=2, row=2,pady= 5, padx=(0, 40))

        # self.btn_add_chart.grid(column=3, row=1, padx=self.padx)
        # self.btn_kill_chart.grid(column=3, row=2, padx=self.padx)
        self.device_check[0].grid(column=4,  row=1, columnspan=1)
        self.device_check[1].grid(column=6,  row=1, columnspan=1)
        self.device_check[2].grid(column=8,  row=1, columnspan=1)
        self.device_check[3].grid(column=10, row=1, columnspan=1)
        self.device_check[4].grid(column=4,  row=2, columnspan=1)
        self.device_check[5].grid(column=6,  row=2, columnspan=1)
        self.device_check[6].grid(column=8,  row=2, columnspan=1)
        self.device_check[7].grid(column=10, row=2, columnspan=1)


        self.btn_start_stream.grid(column=12, row=1, padx=self.padx)
        self.btn_stop_stream.grid(column=12, row=2, padx=self.padx)

        self.save_check.grid(column=13, row=1, columnspan=2)
        # self.separator.place(relx=0.65, rely=0, relwidth=0.001, relheight=1)
        self.separator.place(relx=0.33, rely=-0.1, relwidth=0.001, relheight=1.1)
        self.separator2.place(relx=0.79, rely=-0.1, relwidth=0.001, relheight=1.1)

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
        self.btn_stop_stream["state"] = "active"
        self.btn_start_stream["state"] = "disabled"
        pass

    def stop_stream(self):
        self.btn_start_stream["state"] = "active"
        self.btn_stop_stream["state"] = "disabled"
        pass

    def new_chart(self):
        self.chartMaster.AddChannelMaster()
        pass

    def kill_chart(self):
        pass

    def save_data(self):
        a = 3
        pass


class displayGUI():
    def __init__(self, root, tcp, data) :
        self.root = root
        self.tcp = tcp
        self.data = data
        # self.frame = LabelFrame(root, text="Graphs",
        #                     padx=5, pady=5, bg="white", width=60)
        # self.frame.grid(row=6, column=0, rowspan=20, padx=5, pady=5,sticky=NW)
        
        self.frames = []
        self.framesCol = 0
        self.framesRow = 4
        self.totalFrames = 0

        self.figs = []

        # The control Frame
        self.ControlFrames = []

    def AddChannelMaster(self):
        '''
        This method is a group of methods that will be used to generate a new frame
        that will include a chart and all the control Widgets
        '''
        self.AddMasterFrame()
        self.AddGraph()
        self.AddBtnFrame()

    def AddMasterFrame(self):
        '''
        This Method will add a new master frame wich will control all the element inside
        including the chart, the btns and the Drops
        
        '''
        self.frames.append(LabelFrame(self.root, text=f"Display Manager-{len(self.frames)+1}",
                                      pady=5, padx=5, bg="grey"))
        self.totalframes = len(self.frames)-1
        # print(f'Total frames:{self.totalframes}')
        if self.totalframes % 2 == 0:
            self.framesCol = 0
        else:
            self.framesCol = 20
        # print(f'Col: {self.framesCol}')
        self.framesRow = 4 + 4 * int(self.totalframes / 2)
        # print(f'Row: {self.framesRow}')
        if self.framesCol == 20:
            self.frames[self.totalframes].grid(padx=5,
            column=self.framesCol, row=self.framesRow,columnspan = 20, sticky=N)
        else:

            self.frames[self.totalframes].grid(padx=5,
            column=self.framesCol, row=self.framesRow,columnspan = 20, sticky=NW)
        # else:

        #     self.frames[self.totalframes].grid(padx=5,
        #     column=self.framesCol, row=self.framesRow,columnspan = 16, sticky=NW)

    def AdjustRootFrame(self):
        '''
        This Method will generate the code related to adjusting
        the main root Gui based on the number of added GUI
        '''
        self.totalframes = len(self.frames)-1
        if self.totalframes > 0:
            RootW = 800*2

        else:
            RootW = 800

        if self.totalframes+1 == 0:
            RootH = 120
        else:
            RootH = 120 + 430 * (int(self.totalframes/2)+1)
        self.root.geometry(f"{RootW}x{RootH}")

    def AddGraph(self):
        '''
            This method will add setup the figure and the plot that will be used later on
            All the data will be inside the list to get an easier access later on
            '''
        # Setting up the plot for the each Frame
        self.figs.append([])
        # Initialize figures
        self.figs[self.totalframes].append(plt.Figure(figsize=(7, 5), dpi=80))
        # Initialize the plot
        self.figs[self.totalframes].append(
            self.figs[self.totalframes][0].add_subplot(111))
        # Initialize the chart
        self.figs[self.totalframes].append(FigureCanvasTkAgg(
            self.figs[self.totalframes][0], master=self.frames[self.totalframes]))

        self.figs[self.totalframes][2].get_tk_widget().grid(
            column=1, row=0, columnspan=4, rowspan=17,  sticky=N)

    def AddBtnFrame(self):
        '''
        Method to add the bottons to be used to add further channels 
        the button need to use a partial lib when calling the libary so it can keep the right 
        Widget target --> Further details in the YouTube WeeW-Stack
        '''
        btnH = 2
        btnW = 4
        self.ControlFrames.append([])
        self.ControlFrames[self.totalframes].append(LabelFrame(self.frames[self.totalframes],
                                                            pady=5, bg="white"))
        self.ControlFrames[self.totalframes][0].grid(
            column=0, row=0, padx=5, pady=5,  sticky=N)

        self.ControlFrames[self.totalframes].append(Button(self.ControlFrames[self.totalframes][0], text="+",
                                                        bg="white", width=btnW, height=btnH))
        self.ControlFrames[self.totalframes][1].grid(
            column=0, row=0, padx=5, pady=5)
        self.ControlFrames[self.totalframes].append(Button(self.ControlFrames[self.totalframes][0], text="-",
                                                        bg="white", width=btnW, height=btnH))
        self.ControlFrames[self.totalframes][2].grid(
            column=1, row=0, padx=5, pady=5)


if __name__ == "__main__":
    RootGUI()
    ComGUI()
    ConnGUI()



