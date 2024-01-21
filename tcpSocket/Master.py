from GUI_Master import RootGUI, ComGUI
from tcpserver import TCPServer

RootMaster = RootGUI()

ComMaster = ComGUI(RootMaster.root)

RootMaster.root.mainloop()
