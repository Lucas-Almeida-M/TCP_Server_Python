import re
import numpy as np
import matplotlib
import csv
import time

class DataProcess():
    def __init__(self):
        self.MESSAGETYPE_CONFIG     = 0
        self.MESSAGETYPE_DATA       = 1
        self.MESSAGETYPE_SYNC       = 2
        self.MESSAGETYPE_DISCONNECT = 3
        self.colors = ["blue","orange","green","red","purple","brown","pink","yellow"]
        self.saveData = 0
        self.deviceSyncStatus = {}
        self.deviceSyncCount = {}
        self.clientsData = {}
        pass
    
    def add_client(self, addr):
        self.clientsData[str(addr)] = {}
        self.deviceSyncStatus[str(addr)] = {}
        self.deviceSyncCount[str(addr)] = 0
        pass
    
    def add_device_databuffer(self, addr, id):
        self.clientsData[str(addr)][str(id)] = [[0] * 60 for _ in range(8)]
        pass

    def process_message( self, addr, mes):
            mes = str(mes)
            if mes[0] == "@" and mes[-1] == "!":
                match = re.search(r"@#([^\$]*)#\$([^\$]*)\$&(.*)&!", mes)
                # match = re.search(r"@\$([^\$]*)\$&(.*)&!", mes)
                if match:
                    id = match.group(1)
                    MessageType = int (match.group(2))
                    data = [int(s) for s in (match.group(3).split("&"))]
                    # print(MessageType)
                match MessageType:
                    case self.MESSAGETYPE_CONFIG:
                        
                        
                        pass
                    case self.MESSAGETYPE_DATA:

                        if (str(id) not in self.clientsData[str(addr)]):
                            self.add_device_databuffer(str(addr), id)
                        print ("------------------------------------------")
                        for i in range(8):
                            self.clientsData[str(addr)][str(id)][i] = [int(data[i])] + self.clientsData[str(addr)][str(id)][i][:-1]

                            print(self.clientsData[str(addr)][str(id)][i])
                        
                        if (self.saveData):
                            try:
                                file_path = f"base_de_dados_addr_{str(addr)}.csv"
                                with open(file_path, 'a', newline='') as csv_file:
                                    csv_writer = csv.writer(csv_file)

                                    # If the file is empty, write the header
                                    if csv_file.tell() == 0:
                                        fieldnames = ['time', 'device_id', 'sensor_0', 'sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5', 'sensor_6', 'sensor_7']
                                        csv_writer.writerow(fieldnames)

                                    # Append a new line for each set of values
                                    buffer = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), str(id) ] + list(map(int, data))
                                    
                                    csv_writer.writerow(buffer)

                            except Exception as e:
                                print(f"Error: {e}")
                        print ("------------------------------------------")
                        
                        
                        
                        pass
                    case self.MESSAGETYPE_SYNC:
                        if (str(addr) not in self.clientsData):
                            self.add_client(str(addr))     
                        self.deviceSyncCount[str(addr)] = data[0]
                        for i in range (10):
                            self.deviceSyncStatus[str(addr)][str(i+2)] = data[i+1]
                            if (data[i+1]):
                                if (str(i+2) not in self.clientsData[str(addr)]):
                                    self.add_device_databuffer(addr, i+2)
                                self.deviceSyncStatus[str(addr)][str(i + 2)] = data[i+1]
                            
                        #Tem que ter um if pra saber qual board ta selecionadona dropbox
                        # print(data)
                        # self.GUI.active_devices["text"] = str(self.clientSyncCount[addr])
                        pass
                    case self.MESSAGETYPE_DISCONNECT:
                        pass

                return MessageType, id 
            else:
                return -1  # Error message  

