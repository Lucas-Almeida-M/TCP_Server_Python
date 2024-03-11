import re
import numpy as np
import csv
import os
import time

class DataProcess():
    def __init__(self):
        self.MESSAGETYPE_CONFIG     = 0
        self.MESSAGETYPE_DATA       = 1
        self.MESSAGETYPE_SYNC       = 2
        self.MESSAGETYPE_DISCONNECT = 3
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
        self.clientsData[str(addr)][id] = [[0] * 60 for _ in range(8)]
        pass

    def process_message( self, GUI, addr, mes):
            mes = str(mes)
            if mes[0] == "@" and mes[-1] == "!":
                match = re.search(r"@#([^\$]*)#\$([^\$]*)\$&(.*)&!", mes)
                if match:
                    id = int(match.group(1))
                    MessageType = int (match.group(2))
                    data = [int(i) if self.is_number(i) else i for i in match.group(3).split("&")]
                    if (len(data) == 1 and data[0] == ''):
                        data.pop()
                    # print(MessageType)
                match (MessageType):
                    case self.MESSAGETYPE_CONFIG:
                        
                        
                        pass
                    case self.MESSAGETYPE_DATA:

                        if (id not in self.clientsData[str(addr)]):
                            self.add_device_databuffer(str(addr), id)
                        print ("------------------------------------------")
                        for i in range(8):
                            if data[i] != 'null':
                                self.clientsData[str(addr)][id][i] = [int(data[i])] + self.clientsData[str(addr)][id][i][:-1]
                            else:
                                self.clientsData[str(addr)][id][i] = [0] + self.clientsData[str(addr)][id][i][:-1]
                            # print(self.clientsData[str(addr)][id][i])
                        print(f"Data from id {id}")
                        
                        if (self.saveData):
                            try:
                                file_path = f"client_{str(addr)}/base_de_dados_id_{str(id)}.csv"
                                with open(file_path, 'a', newline='') as csv_file:
                                    csv_writer = csv.writer(csv_file)

                                    if csv_file.tell() == 0:
                                        fieldnames = ['time', 'device_id', 'sensor_0', 'sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5', 'sensor_6', 'sensor_7']
                                        csv_writer.writerow(fieldnames)
                                    
                                    buffer = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), str(id) ] + list(map(lambda x: int(x) if self.is_number(x) else "-", data))
                                    
                                    csv_writer.writerow(buffer)

                            except Exception as e:
                                print(f"Error: {e}")
                        print ("------------------------------------------")

                        GUI.update_graph(addr, id)
                        pass

                    case self.MESSAGETYPE_SYNC:
                        if (str(addr) not in self.clientsData):
                            self.add_client(str(addr)) 
                        self.deviceSyncCount[str(addr)] = len(data)
                        self.deviceSyncStatus[str(addr)] = [] # clear the indexes
                        for i in range (len(data)):
                            self.deviceSyncStatus[str(addr)].append(int(data[i]))
                            if ( data[i] not in self.clientsData[str(addr)]):
                                self.add_device_databuffer(addr, data[i])   
                        GUI.gui_sync_update(addr)
                     
                        pass

                    case self.MESSAGETYPE_DISCONNECT:
                        pass

                return MessageType, id 
            else:
                return -1  
    def is_number(self, num):
        try:
            int(num)  
            return True
        except ValueError:
            return False
        
    def create_client_folder(self, addr):
        if not os.path.exists(f"client_{str(addr)}"):
            os.makedirs(f"client_{str(addr)}", exist_ok=True)

