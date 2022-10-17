import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
#from tkinter.messagebox import showinfo


class gui():
    filepath = ""
    codingType = 0
    root = None

    def __init__(self):
        pass

    def selectTextFile():
        # file type
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        # show the open file dialog
        gui.filepath = fd.askopenfilename(filetypes=filetypes)
        #showinfo(title='Selected File', message=gui.filepath)

    def encodeButton():
        gui.codingType = 0
        gui.root.destroy()

    def decodeButton():
        gui.codingType = 1
        gui.root.destroy()

    def getUserInput(self, inputType):
        if(inputType == 1):  # 1. Console Arguments
            if(len(sys.argv) < 3):
                sys.exit("To few arguments! At least 2 are needed.")
            elif(len(sys.argv) > 3):
                sys.exit("To many arguments! Only 2 are allowed.")

            gui.filepath = sys.argv[1]  # input filepath
            gui.codingType = int(sys.argv[2])  # input number 0/1
        elif(inputType == 2):  # 2. Console Input
            gui.filepath = input(prompt="Filepath: ")
            gui.codingType = int(input(prompt="Coding Type: "))
        elif(inputType == 3):  # 3. GUI Input
            gui.root = Tk()
            frm = ttk.Frame(gui.root, padding=10)
            frm.grid()
            ttk.Button(frm, text='Select a File',
                       command=gui.selectTextFile).grid(column=1, row=0)
            ttk.Button(frm, text="Encode", command=gui.encodeButton).grid(
                column=0, row=1)
            ttk.Button(frm, text="Decode", command=gui.decodeButton).grid(
                column=1, row=1)
            gui.root.mainloop()

        return gui.codingType, gui.filepath
