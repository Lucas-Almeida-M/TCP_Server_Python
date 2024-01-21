from GUI_Master import RootGUI, ComGUI
from tcpserver import TCPServer

RootMaster = RootGUI()

TcpServer = TCPServer()

ComMaster = ComGUI(RootMaster.root, TcpServer)

RootMaster.root.mainloop()
