import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("Data visualizer")
        #setting window size
        width=1135
        height=678
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GListBox_970=tk.Listbox(root)
        GListBox_970["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_970["font"] = ft
        GListBox_970["fg"] = "#333333"
        GListBox_970["justify"] = "center"
        GListBox_970.place(x=430,y=610,width=241,height=30)
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
