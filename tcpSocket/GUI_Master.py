import os
import signal
import numpy as np
from tkinter import *
from tkinter import ttk
import re
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

class RootGUI():
    def __init__(self):
        self.root = Tk()
        self.root.title("Data vizualizer")
        self.root.geometry("1500x1000")
        self.root.config(bg="white")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        print("Program closed")
        os.kill(os.getpid(), signal.SIGTERM)
        self.root.destroy()
        exit(2)
        
# Classe de comunicação com o microcontrolador
class ComGUI():
    
    def __init__(self, root, tcp, data):
        self.root = root
        self.tcp = tcp
        self.data = data
        self.frame = LabelFrame(root, text="Tcp Socket",
                                padx=5, pady=5, bg="white")
        self.server_ip = Label(
            self.frame, text="Server IP: ", bg="white", width=15, anchor="w")
        self.server_port = Label(
            self.frame, text="Server Port: ", bg="white", width=15, anchor="w")


        self.ServerIPOptionMenu()
        self.btn_connect = Button(self.frame, text="Start Server",
                                  width=10, state="active",  command=self.tcp_connect)

        self.padx = 20
        self.pady = 5

        self.publish()

    def publish(self):
        self.frame.grid(row=0, column=0, rowspan=3,
                        columnspan=3, padx=5, pady=5)
        self.server_ip.grid(column=1, row=2)
        self.server_port.grid(column=1, row=3)

        self.IPselect.grid(column=2, row=2, padx=self.padx, pady=self.pady)
        self.Portselect.grid(column=2, row=3, padx=self.padx, pady=self.pady)

        self.btn_connect.grid(column=3, row=2)

    def ServerIPOptionMenu(self):
        self.IPselect = Entry(self.frame, width=30)
        self.Portselect = Entry(self.frame, width=30)

        self.IPselect.insert(0,"192.168.0.100")
        self.Portselect.insert(0,"8000")

    def tcp_connect(self):
        if (self.btn_connect['text'] == 'Start Server'):
            ip = self.IPselect.get()
            port = int (self.Portselect.get())
            if self.is_valid_ip_format(ip) and (( port > 1000) and (port< 65535 )):
                print(f"TRYING TO CONNECT TO SERVER  IP {ip} port {port}")
                try:
                    self.conn = ConnGUI(self.root, self.tcp, self.data)
                    self.tcp.start(ip, port, self.conn, self.data)
                    self.btn_connect['text'] = "Stop Server"
                except Exception as e:
                    print(f"Error: {e}")
        else:
            self.tcp.stop()
            self.conn.frame.destroy()
            self.btn_connect["text"] = "Start Server"

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
        self.board = 0
        self.colors = ["blue","orange","green","red","purple","brown","pink","yellow"]
        self.frame = LabelFrame(root, text="Connection Manager",
                            padx=5, pady=5, bg="white", width=60)
        self.bds = []
        self.drop_bds_label = Label(
            self.frame, text="Board Select: ", bg="white", width=15, anchor="w")
        self.BoardSelectionMenu("default")

        self.active_devices_label = Label(    
            self.frame, text="Active Devices: ", bg="white", width=15, anchor="w")
        self.active_devices = Label(
            self.frame, text="0", bg="white", fg="orange", width=5)

        self.device_check = {}
        self.device_check_var = {}
        self.device_check_active = []
        self.saved_sensor_check_vars = {}

        self.device_check_var[2] = IntVar()
       
        self.device_check[2] = ( Checkbutton(self.frame, text="device [2]", variable=self.device_check_var[2],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=lambda : self.chart_manager(2)))
        
        self.device_check_var[3] = IntVar()
        self.device_check[3] = ( Checkbutton(self.frame, text="device [3]", variable=self.device_check_var[3],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=lambda : self.chart_manager(3)) )
        
        self.device_check_var[4] = IntVar()
        self.device_check[4] = ( Checkbutton(self.frame, text="device [4]", variable=self.device_check_var[4],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=lambda : self.chart_manager(4)))
        
        self.device_check_var[5] = IntVar()
        self.device_check[5] = ( Checkbutton(self.frame, text="device [5]", variable=self.device_check_var[5],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=lambda : self.chart_manager(5)))
        
        self.device_check_var[6] = IntVar()
        self.device_check[6] = ( Checkbutton(self.frame, text="device [6]", variable=self.device_check_var[6],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=lambda : self.chart_manager(6)))
        
        self.device_check_var[7] = IntVar()
        self.device_check[7] = ( Checkbutton(self.frame, text="device [7]", variable=self.device_check_var[7],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=lambda : self.chart_manager(7)))
        
        self.device_check_var[8] = IntVar()
        self.device_check[8] = ( Checkbutton(self.frame, text="device [8]", variable=self.device_check_var[8],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=lambda : self.chart_manager(8)))
        
        self.device_check_var[9] = IntVar()
        self.device_check[9] = ( Checkbutton(self.frame, text="device [9]", variable=self.device_check_var[9],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=lambda : self.chart_manager(9)))
        
        self.device_check_var[10] = IntVar()
        self.device_check[10] = ( Checkbutton(self.frame, text="device [10]", variable=self.device_check_var[10],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=lambda : self.chart_manager(10)))
        
        self.device_check_var[11] = IntVar()
        self.device_check[11] = ( Checkbutton(self.frame, text="device [11]", variable=self.device_check_var[11],
                                    onvalue=1, offvalue=0, bg="white", state="disabled",
                                    command=lambda : self.chart_manager(11)))
        


        self.btn_options = Button(self.frame, text="Options", state="disabled",
                                    width=7, command=self.new_chart)
        
        self.save = False
        self.SaveVar = IntVar()
        self.save_check = Checkbutton(self.frame, text="Save data", variable=self.SaveVar,
                                    onvalue=1, offvalue=0, bg="white", state="active",
                                    command=self.save_data)

        self.separator = ttk.Separator(self.frame, orient='vertical')
        self.separator2 = ttk.Separator(self.frame, orient='vertical')
        
        self.padx = (40,5)
        self.pady = (40,5)

        self.ConnGUIOpen()

        
        self.chartMaster = displayGUI(self.root, self.tcp, self.data, self)

        
    def ConnGUIOpen(self):

        self.frame.grid(row=0, column=3, rowspan=3,
                        columnspan=18, padx=5, pady=5, sticky='nsew')

        self.drop_bds_label.grid(column=1, row=1)
        self.drop_bds.grid(column=2, row=1, padx=(0, 40))

        self.active_devices_label.grid(column=1, row=2)
        self.active_devices.grid(column=2, row=2,pady= 5, padx=(0, 40))

        self.device_check[2].grid(column=4,  row=1, columnspan=1)
        self.device_check[3].grid(column=6,  row=1, columnspan=1)
        self.device_check[4].grid(column=8,  row=1, columnspan=1)
        self.device_check[5].grid(column=10, row=1, columnspan=1)
        self.device_check[6].grid(column=12, row=1, columnspan=1)
        self.device_check[7].grid(column=4,  row=2, columnspan=1)
        self.device_check[8].grid(column=6,  row=2, columnspan=1)
        self.device_check[9].grid(column=8,  row=2, columnspan=1)
        self.device_check[10].grid(column=10, row=2, columnspan=1)
        self.device_check[11].grid(column=12, row=2, columnspan=1)

        self.btn_options.grid(column=13, row=1, padx=self.padx)
        self.save_check.grid(column=14, row=1, columnspan=2)
        self.separator.place(relx=0.285, rely=-0.1, relwidth=0.001, relheight=1.1)
        self.separator2.place(relx=0.813, rely=-0.1, relwidth=0.001, relheight=1.1)

    def BoardSelectionMenu(self, arg):
        if arg == "default":
            self.bds = ["-"]
            self.clicked_bds = StringVar(value=self.bds[0])
            self.drop_bds = OptionMenu(self.frame, self.clicked_bds, *self.bds, command=self.BoardSelectionAdjust)
            self.drop_bds.config(width=10)
        else:
            self.bds.append(arg)
            self.bds[:] = [x for x in self.bds if x != "-"]
            self.clicked_bds.set(self.bds[0])
            self.drop_bds.destroy()
            self.drop_bds = OptionMenu(self.frame, self.clicked_bds, *self.bds, command=self.BoardSelectionAdjust)
            self.drop_bds.config(width=10)

            self.drop_bds_label.grid(column=1, row=1)
            self.drop_bds.grid(column=2, row=1, padx=(0, 40))

    def gui_sync_update(self, addr):
        self.active_devices["text"] = self.data.deviceSyncCount[addr]
        for i in range (2,12):
            if i in self.data.deviceSync[addr]:
                 self.device_check[i]["state"] = "active"
            else:
                self.device_check[i]["state"] = "disabled"
                if (self.device_check_var[i].get() == 1):
                    self.device_check_var[i].set(0)
                    self.chart_manager(i)
        pass

    def update_graph(self, addr, id):
        if ( id in self.device_check_active):
            self.chartMaster.figs[self.device_check_active.index(id)][1].clear()
            X_data = list (i for i in range (60))
            self.chart = self.chartMaster.figs[self.device_check_active.index(id)][1]
            for i in range (8):
                if (self.chartMaster.ControlFrames[self.device_check_active.index(id)][1][i].get()):
                    Y_data = self.data.clientsData[addr][id][i]
                    self.chart.plot(X_data, Y_data, color=self.colors[i],
                        dash_capstyle='projecting', linewidth=1)
            self.chart.set_xlabel('Temperatura')
            self.chart.set_ylabel('Tempo')
            self.chartMaster.figs[self.device_check_active.index(id)][1].grid(
                    color='b', linestyle='-', linewidth=0.2)
            self.chartMaster.figs[self.device_check_active.index(id)][0].canvas.draw()

        pass

    def BoardSelectionAdjust(self, widget):
        self.board = self.clicked_bds.get()
        print (f"Board selected {self.board}")

    def ConnGUIClose(self):

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

    def chart_manager(self, num):
    
        #Destroy the frames
        for i in range(len(self.device_check_active)):
            self.chartMaster.frames[i].destroy()
        self.chartMaster.frames = []
        self.chartMaster.figs = []
        self.chartMaster.ControlFrames = []

        # Create it again 
        if (self.device_check_var[num].get()):
            self.device_check_active.append(num)
            if num not in self.saved_sensor_check_vars:
                self.saved_sensor_check_vars[num] = [] 
                for i in range (8):
                    self.saved_sensor_check_vars[num].append(IntVar())
        else:
            self.device_check_active.remove(num)
            del self.saved_sensor_check_vars[num]

        self.device_check_active.sort()
        for i in range(len(self.device_check_active)):
            self.new_chart(self.device_check_active[i], self.saved_sensor_check_vars[self.device_check_active[i]])
        

        if (len(self.device_check_active) == 4):
            for i in range (10):
                if(i not in self.device_check_active):
                    self.device_check[i]["state"] = "disabled"
        # else:
        #     # for i in range (2,12):
        #     #     self.device_check[i]["state"] = "active"
        # pass

    def new_chart(self, num, saved):
        self.chartMaster.AddChannelMaster(num, saved)
        pass

    def kill_chart(self, num):
        try:
            if len(self.chartMaster.frames) > 0:
                totalFrame = len(self.chartMaster.frames)-1
                self.chartMaster.frames[totalFrame].destroy()
                self.chartMaster.frames.pop()
                self.chartMaster.figs.pop()
                self.chartMaster.ControlFrames.pop()
        except:
            pass

        pass

    def save_data(self):
        self.data.saveData = self.SaveVar.get()
        pass


class displayGUI():
    def __init__(self, root, tcp, data, conn) :
        self.root = root
        self.tcp = tcp
        self.data = data
        self.conn = conn

        self.sensortypes = ['Temperatura','Tensão','Pressão']

        self.frames = []
        self.framesCol = 0
        self.framesRow = 4
        self.totalFrames = 0

        self.figs = []

        # The control Frame
        self.ControlFrames = []

    def AddChannelMaster(self, num, saved):
 
        self.AddMasterFrame(num)
        self.AddGraph()
        self.add_sensor_check_frame(num, saved)
        
    def AddMasterFrame(self,num):
      
        self.frames.append(LabelFrame(self.root, text=f"[can ID: {num}]",
                                      pady=5, padx=5, bg="white"))
        self.totalframes = len(self.frames)-1

        if self.totalframes % 2 == 0:
            self.framesCol = 0
        else:
            self.framesCol = 20
    
        self.framesRow = 4 + 4 * int(self.totalframes / 2)
   
        if self.framesCol == 20:
            self.frames[self.totalframes].grid(padx=5,
            column=self.framesCol, row=self.framesRow,columnspan = 20, sticky=N)
        else:

            self.frames[self.totalframes].grid(padx=5,
            column=self.framesCol, row=self.framesRow,columnspan = 20, sticky=NW)


    def AdjustRootFrame(self):

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
        self.figs.append([])

        self.figs[self.totalframes].append(plt.Figure(figsize=(8, 5), dpi=80))
        self.figs[self.totalframes].append(
            self.figs[self.totalframes][0].add_subplot(111))

        self.figs[self.totalframes].append(FigureCanvasTkAgg(
            self.figs[self.totalframes][0], master=self.frames[self.totalframes]))

        self.figs[self.totalframes][2].get_tk_widget().grid(
            column=1, row=0, columnspan=4, rowspan=17,  sticky=N)

    def add_sensor_check_frame(self, num, saved):
        self.ControlFrames.append([])
        
        self.ControlFrames[self.totalframes].append(LabelFrame(self.frames[self.totalframes],
                                                            pady=5, bg="white"))
        self.ControlFrames[self.totalframes][0].grid(
            column=0, row=0, padx=5, pady=5,  sticky=N)
        
        self.ControlFrames[self.totalframes].append([])
        
        for i in range (8):
            self.ControlFrames[self.totalframes][1].append(saved[i])

        self.ControlFrames[self.totalframes].append( Checkbutton(self.ControlFrames[self.totalframes][0], text="Sensor 0", variable=self.ControlFrames[self.totalframes][1][0],
                                    onvalue=1, offvalue=0, bg="white", state="active",
                                    command=self.ButtonSensorFunc))
        self.ControlFrames[self.totalframes].append( Checkbutton(self.ControlFrames[self.totalframes][0], text="Sensor 1", variable=self.ControlFrames[self.totalframes][1][1],
                                    onvalue=1, offvalue=0, bg="white", state="active",
                                    command=self.ButtonSensorFunc))
        self.ControlFrames[self.totalframes].append( Checkbutton(self.ControlFrames[self.totalframes][0], text="Sensor 2", variable=self.ControlFrames[self.totalframes][1][2],
                                    onvalue=1, offvalue=0, bg="white", state="active",
                                    command=self.ButtonSensorFunc))
        self.ControlFrames[self.totalframes].append( Checkbutton(self.ControlFrames[self.totalframes][0], text="Sensor 3", variable=self.ControlFrames[self.totalframes][1][3],
                                    onvalue=1, offvalue=0, bg="white", state="active",
                                    command=self.ButtonSensorFunc))
        self.ControlFrames[self.totalframes].append( Checkbutton(self.ControlFrames[self.totalframes][0], text="Sensor 4", variable=self.ControlFrames[self.totalframes][1][4],
                                    onvalue=1, offvalue=0, bg="white", state="active",
                                    command=self.ButtonSensorFunc))
        self.ControlFrames[self.totalframes].append( Checkbutton(self.ControlFrames[self.totalframes][0], text="Sensor 5", variable=self.ControlFrames[self.totalframes][1][5],
                                    onvalue=1, offvalue=0, bg="white", state="active",
                                    command=self.ButtonSensorFunc))
        self.ControlFrames[self.totalframes].append( Checkbutton(self.ControlFrames[self.totalframes][0], text="Sensor 6", variable=self.ControlFrames[self.totalframes][1][6],
                                    onvalue=1, offvalue=0, bg="white", state="active",
                                    command=self.ButtonSensorFunc))
        self.ControlFrames[self.totalframes].append( Checkbutton(self.ControlFrames[self.totalframes][0], text="Sensor 7", variable=self.ControlFrames[self.totalframes][1][7],
                                    onvalue=1, offvalue=0, bg="white", state="active",
                                    command=self.ButtonSensorFunc))
        self.ControlFrames[self.totalframes].append(Button(self.ControlFrames[self.totalframes][0], text="Config", state="active",
                                    width=7, command=lambda : self.device_config(num)))
        self.ControlFrames[self.totalframes].append(Button(self.ControlFrames[self.totalframes][0], text="Status", state="active",
                                    width=7, command=lambda : self.device_status(num)))
        
        canvas = []
        canvas.append(Canvas(self.ControlFrames[self.totalframes][0], width=10, height=10))
        canvas[0].create_rectangle(0, 10, 10, 0, fill=self.conn.colors[0])

        canvas.append(Canvas(self.ControlFrames[self.totalframes][0], width=10, height=10))
        canvas[1].create_rectangle(0, 10, 10, 0, fill=self.conn.colors[1])

        canvas.append(Canvas(self.ControlFrames[self.totalframes][0], width=10, height=10))
        canvas[2].create_rectangle(0, 10, 10, 0, fill=self.conn.colors[2])

        canvas.append(Canvas(self.ControlFrames[self.totalframes][0], width=10, height=10))
        canvas[3].create_rectangle(0, 10, 10, 0, fill=self.conn.colors[3])

        canvas.append(Canvas(self.ControlFrames[self.totalframes][0], width=10, height=10))
        canvas[4].create_rectangle(0, 10, 10, 0, fill=self.conn.colors[4])

        canvas.append(Canvas(self.ControlFrames[self.totalframes][0], width=10, height=10))
        canvas[5].create_rectangle(0, 10, 10, 0, fill=self.conn.colors[5])

        canvas.append(Canvas(self.ControlFrames[self.totalframes][0], width=10, height=10))
        canvas[6].create_rectangle(0, 10, 10, 0, fill=self.conn.colors[6])

        canvas.append(Canvas(self.ControlFrames[self.totalframes][0], width=10, height=10))
        canvas[7].create_rectangle(0, 10, 10, 0, fill=self.conn.colors[7])

        canvas[0].grid(column=2, row=0, padx=5, pady=5)
        canvas[1].grid(column=2, row=1, padx=5, pady=5)
        canvas[2].grid(column=2, row=2, padx=5, pady=5)
        canvas[3].grid(column=2, row=3, padx=5, pady=5)
        canvas[4].grid(column=2, row=4, padx=5, pady=5)
        canvas[5].grid(column=2, row=5, padx=5, pady=5)
        canvas[6].grid(column=2, row=6, padx=5, pady=5)
        canvas[7].grid(column=2, row=7, padx=5, pady=5)
        
        self.ControlFrames[self.totalframes][2].grid(
            column=1, row=0, padx=5, pady=5)
        self.ControlFrames[self.totalframes][3].grid(
            column=1, row=1, padx=5, pady=5)
        self.ControlFrames[self.totalframes][4].grid(
            column=1, row=2, padx=5, pady=5)
        self.ControlFrames[self.totalframes][5].grid(
            column=1, row=3, padx=5, pady=5)
        self.ControlFrames[self.totalframes][6].grid(
            column=1, row=4, padx=5, pady=5)
        self.ControlFrames[self.totalframes][7].grid(
            column=1, row=5, padx=5, pady=5)
        self.ControlFrames[self.totalframes][8].grid(
            column=1, row=6, padx=5, pady=5)
        self.ControlFrames[self.totalframes][9].grid(
            column=1, row=7, padx=5, pady=5)
        self.ControlFrames[self.totalframes][10].grid(
            column=1, row=8, padx=5, pady=5)
        self.ControlFrames[self.totalframes][11].grid(
            column=1, row=9, padx=5, pady=5)
        

    def device_config(self, id):
        # print('config')
        self.extra_window = Toplevel()
        self.extra_window.title = 'Config'
        self.extra_window.geometry ('250x100')
        
        self.id_label = Label(self.extra_window, text="ID : ", bg="white", width=15, anchor="w")
        self.sensors_enabled_label = Label(self.extra_window, text="Sensors Enabled : ", bg="white", width=15, anchor="w")
        self.id_selected = Entry(self.extra_window, width=30)
        self.sensors_enabled_selected = Entry(self.extra_window, width=30)

        self.id_selected.insert(0, id)
        self.sensors_enabled_selected.insert(0,"teste")

        self.button_config = Button(self.extra_window, text="Apply Config", state="active", width=10, command=self.applyconfig)

        self.id_label.grid(column=0, row=0, padx=5, pady=5)
        self.sensors_enabled_label.grid(column=0, row=1, padx=5, pady=5)
        self.id_selected.grid(column=1, row=0, padx=5, pady=5)
        self.sensors_enabled_selected.grid(column=1, row=1, padx=5, pady=5)
        self.button_config.grid(column=0, row=2, padx=5, pady=5)
       
        pass

    def applyconfig (self):
        message_type = self.data.MESSAGETYPE_CONFIG 
        changed_id = self.id_selected.get()
        sensors_active = self.sensors_enabled_selected.get()

        msg = f"@#{id}#${message_type}$&{changed_id}&{sensors_active}&!"
        self.tcp.send_message(msg, self.board)

        pass

    def device_status(self, id):
        self.extra_window = Toplevel()
        self.extra_window.title = 'Config'
        self.extra_window.geometry ('250x200')

        sens_hab = Label(self.extra_window, text="Tipo de sensor : ", bg="white", width=15, anchor="w")
        sens_hab_text = Label(self.extra_window, text=self.sensortypes[self.data.DeviceStatus[self.conn.board][str(id)]['sensortype']], bg="white", width=15, anchor="w")

        intern_temp = Label(self.extra_window, text="Temperatura Interna [C]: ", bg="white", width=15, anchor="w")
        intern_temp_text = Label(self.extra_window, text=self.data.DeviceStatus[self.conn.board][str(id)]['internalTemp'], bg="white", width=15, anchor="w")

        trans_error = Label(self.extra_window, text="Erros de transmissão : ", bg="white", width=15, anchor="w")
        trans_error_text = Label(self.extra_window, text=self.data.DeviceStatus[self.conn.board][str(id)]['transmissionErrors'], bg="white", width=15, anchor="w")

        temp_func = Label(self.extra_window, text="Tempo de funcionamento [h] : ", bg="white", width=15, anchor="w")
        temp_func_text = Label(self.extra_window, text=self.data.DeviceStatus[self.conn.board][str(id)]['runtime'], bg="white", width=15, anchor="w")

        sens_hab.grid(column=0, row=0, padx=5, pady=5)
        sens_hab_text.grid(column=1, row=0, padx=5, pady=5)
        intern_temp.grid(column=0, row=1, padx=5, pady=5)
        intern_temp_text.grid(column=1, row=1, padx=5, pady=5)
        trans_error.grid(column=0, row=2, padx=5, pady=5)
        trans_error_text.grid(column=1, row=2, padx=5, pady=5)
        temp_func.grid(column=0, row=3, padx=5, pady=5)
        temp_func_text.grid(column=1, row=3, padx=5, pady=5)

        pass

    def clear_sensor_check(self, num):

        pass

    def ButtonSensorFunc(self):
        
        pass
    
    
if __name__ == "__main__":
    RootGUI()
    ComGUI()
    ConnGUI()



