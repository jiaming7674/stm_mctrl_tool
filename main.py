import numpy as np
import tkinter as tk
from tkinter import ttk

from serial_port import COMPort
from scope import Scope


class mainGUI():

    def __init__(self):
        
        self.window = tk.Tk()
        self.window.title("Test GUI")

        self.ssop = Scope()

        self.ssop.callback = self.readFromSerialPort

        self.comState = False

        self.com_port = COMPort()

        # a frame contains COM's information, and start/stop button
        frame_COMinf = tk.Frame(self.window)
        frame_COMinf.grid(row=1, column=1)

        labelCOM = tk.Label(frame_COMinf, text="COMx: ")
        self.COM = tk.StringVar(value="COM4")
        entryCOM = tk.Entry(frame_COMinf, textvariable = self.COM)
        labelCOM.grid(row=1, column=1, padx=5, pady=3)
        entryCOM.grid(row=1, column=2, padx=5, pady=3)


        self.buttonSS = tk.Button(frame_COMinf, text="Start", command=self.processButtonSS)
        self.buttonSS.grid(row=1, column=3, padx=5, pady=3)

        self.buttonScope = tk.Button(frame_COMinf, text="Scope", command=self.processButtonOpenScope)
        self.buttonScope.grid(row=1, column=4, padx=5, pady=3, sticky=tk.E)

        # received data frame
        frameRecv = tk.Frame(self.window)
        frameRecv.grid(row=2, column=1)
        labelOutText = tk.Label(frameRecv, text="Received Data:")
        labelOutText.grid(row=1, column=1, padx=5, pady=3, sticky=tk.W)

        frameRecvSon = tk.Frame(frameRecv)
        frameRecvSon.grid(row=2, column=1)
        scrollbarRecv = tk.Scrollbar(frameRecvSon)
        scrollbarRecv.grid(row=2, column=1, padx=5, pady=3)
        scrollbarRecv.pack(side=tk.RIGHT, fill=tk.Y)

        self.OutputText = tk.Text(frameRecvSon, wrap=tk.WORD, width=60, height=20, yscrollcommand = scrollbarRecv.set)
        self.OutputText.pack()

        frameTrans = tk.Frame(self.window)
        frameTrans.grid(row=3, column=1)
        labelInText = tk.Label(frameTrans, text="To Transmit Data:")
        labelInText.grid(row=1, column=1, padx=5, pady=3, sticky=tk.W)
        frameTransSon = tk.Frame(frameTrans)
        frameTransSon.grid(row=2, column=1)
        scrollbarTrans=tk.Scrollbar(frameTransSon)
        scrollbarTrans.pack(side=tk.RIGHT, fill=tk.Y)
        self.InputText=tk.Text(frameTransSon, wrap=tk.WORD, width=60, height=5, yscrollcommand=scrollbarTrans.set)
        self.InputText.pack(side='top')

        self.entry1=tk.Entry(frameTransSon, textvariable='0')
        self.entry1.pack(side='left')

        self.buttonSend = tk.Button(frameTrans, text="Send", command=self.processButtonSend)
        self.buttonSend.grid(row=3, column=1, padx=5, pady=3, sticky=tk.E)

        self.window.mainloop()


    def processButtonSS(self):
        
        if (self.comState):
            if self.com_port.close() == True:
                self.comState = False
                self.buttonSS["text"] = "Start"

        else:
            if self.com_port.open() == True:
                self.comState = True
                self.buttonSS["text"] = "Stop"

    def processButtonSend(self):
        if (self.comState):
            stext = self.entry1.get()

            val = int(stext)

            bytesToSend = int.to_bytes(val, length=12, byteorder='little')
            print(bytesToSend)
            self.com_port.serial_port.write(bytesToSend)

    def processButtonOpenScope(self):
        if (self.comState):

            self.ssop.start()


    def readFromSerialPort(self):
        data = []

        if (self.comState):
            while(self.com_port.is_buffer_not_empty()):
                data.append(self.com_port.read_from_buffer())

        return data


    def quit(self):
        self.com_port.close()
        self.window.destroy()


if __name__ == '__main__':

    app = mainGUI()