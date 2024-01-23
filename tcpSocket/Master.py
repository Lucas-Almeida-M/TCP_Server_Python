from GUI_Master import RootGUI, ComGUI
from tcpserver import TCPServer
from Data_Processing import DataProcess

RootMaster = RootGUI()

TcpServer = TCPServer()

Data = DataProcess()

ComMaster = ComGUI(RootMaster.root, TcpServer, Data)

RootMaster.root.mainloop()
