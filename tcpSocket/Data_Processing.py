import re
import numpy as np
import matplotlib

class DataProcess():
    def __init__(self):
        self.MESSAGETYPE_CONFIG     = 0
        self.MESSAGETYPE_DATA       = 1
        self.MESSAGETYPE_SYNC       = 2
        self.MESSAGETYPE_DISCONNECT = 3
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
        self.clientsData[str(addr)][str(id)] = [[0] * 64 for _ in range(8)]
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

                return MessageType    
            else:
                return -1  # Error message  

