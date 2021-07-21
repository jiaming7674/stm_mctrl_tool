import numpy as np
import tkinter as tk
from tkinter import ttk
import threading
from communication_protocol import CommunicationProtocol
from scope import Scope

import time
import threading

class mainGUI():

    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Motor Tool")

        self.comState = False

        self.com_protocol = CommunicationProtocol()
        self.scope = Scope()
        self.scope.callback = self.readFromSerialPort


        # COM Information Frame =====================================
        frame_COMinf = tk.Frame(self.window)
        frame_COMinf.grid(row=0, column=0)

        labelCOM = tk.Label(frame_COMinf, text="COMx: ")
        self.COM = tk.StringVar(value="COM4")
        entryCOM = tk.Entry(frame_COMinf, textvariable=self.COM)

        labelBaudrate = tk.Label(frame_COMinf, text="Baudrate: ")
        self.Baudrate = tk.IntVar(value=115200)
        entryBaudrate = tk.Entry(frame_COMinf, textvariable=self.Baudrate)

        labelParity = tk.Label(frame_COMinf, text="Parity: ")
        self.Parity = tk.StringVar(value="NONE")
        comboParity = ttk.Combobox(frame_COMinf, width=17, textvariable=self.Parity)
        comboParity["values"] = ("NONE","ODD","EVEN","MARK","SPACE")
        comboParity["state"] = "readonly"

        labelStopbits = tk.Label(frame_COMinf, text="Stopbits: ")
        self.Stopbits = tk.StringVar(value="1")
        comboStopbits = ttk.Combobox(frame_COMinf, width=17, textvariable=self.Stopbits)
        comboStopbits["values"] = ("1", "1.5", "2")
        comboStopbits["state"] = "readonly"
        self.buttonSS = tk.Button(frame_COMinf, text="COM Open", command=self.processButtonSS)

        labelCOM.grid(row=0, column=0, padx=5, pady=3)
        entryCOM.grid(row=0, column=1, padx=5, pady=3)
        labelBaudrate.grid(row=0, column=2, padx=5, pady=3)
        entryBaudrate.grid(row=0, column=3, padx=5, pady=3)
        labelParity.grid(row=1, column=0, padx=5, pady=3)
        comboParity.grid(row=1, column=1, padx=5, pady=3)
        labelStopbits.grid(row=1, column=2, padx=5, pady=3)
        comboStopbits.grid(row=1, column=3, padx=5, pady=3)
        self.buttonSS.grid(row=1, column=4, padx=5, pady=3)

        # Motor Information Frame
        frameMotorInfo = tk.Frame(self.window)
        frameMotorInfo.grid(row=1, column=0)

        labelConnection = tk.Label(frameMotorInfo, text="Connection: ")
        entryConnection = tk.Entry(frameMotorInfo, textvariable=tk.StringVar(value='Not Connected'))
        labelStatus = tk.Label(frameMotorInfo, text="Status: ")
        entryStatus = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))
        labelError = tk.Label(frameMotorInfo, text="Error: ")
        entryError = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))

        labelConnection.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W+tk.E+tk.S+tk.N)
        entryConnection.grid(row=0, column=1, padx=5, pady=3)
        labelStatus.grid(row=0, column=2, padx=5, pady=3)
        entryStatus.grid(row=0, column=3, padx=5, pady=3)
        labelError.grid(row=0, column=4, padx=5, pady=3)
        entryError.grid(row=0, column=5, padx=5, pady=3)

        # Control Frame ==================================================

        frameControl = tk.Frame(self.window)
        frameControl.grid(row=2, column=0)

        labelSpeed = tk.Label(frameControl, text="Set Speed: ")
        self.entrySpeed = tk.Entry(frameControl, textvariable=tk.IntVar(value='0'))

        self.buttonSetSpeed = tk.Button(frameControl, text="Set", command=self.processButtonSend, width = 10)
        self.buttonMotorStart = tk.Button(frameControl, text="Run", command=self.processButtonMotorStart, width = 10, bg='green')
        self.buttonMotorStop = tk.Button(frameControl, text="Stop", command=self.processButtonMotorStop, width = 10, bg='red')

        labelSpeed.grid(row=0, column=0, padx=5, pady=3)
        self.entrySpeed.grid(row=0, column=1, padx=5, pady=3)
        self.buttonSetSpeed.grid(row=0, column=2, padx=5, pady=3)
        self.buttonMotorStart.grid(row=0, column=3, padx=10, pady=3, sticky=tk.E)
        self.buttonMotorStop.grid(row=0, column=4, padx=10, pady=3, sticky=tk.E)


        # Debug Frame ==================================================
        frameDebug = tk.Frame(self.window)
        frameDebug.grid(row=3, column=0)

        # labelD1 = tk.Label(frameDebug, text="D1: ")
        # labelD2 = tk.Label(frameDebug, text="D2: ")
        # labelD3 = tk.Label(frameDebug, text="D3: ")

        self.labelDebug = []
        self.entryDebug = []

        for i in range(5):
            self.labelDebug.append(tk.Label(frameDebug, text='D'+ str(i) + ': '))
            self.entryDebug.append(tk.Entry(frameDebug, textvariable=tk.IntVar(value=0)))

            self.labelDebug[i].grid(row=i, column=0, padx=5, pady=3)
            self.entryDebug[i].grid(row=i, column=1, padx=5, pady=3)

        self.buttonScope = tk.Button(frameDebug, text="Scope ON", command=self.processButtonScope)

        self.buttonScope.grid(row=0, column=2)

        # Test Frame ==================================================

        frameTest = tk.Frame(self.window)
        frameTest.grid(row=4, column=0)

        self.labelTest = tk.Label(frameTest, text="Test : ", bg='yellow')
        self.labelTest.grid(row=0, column=0, padx=5, pady=3)
        #labelTest.pack(side='left')

        self.EntryTest1 = tk.Entry(frameTest)
        self.EntryTest1.grid(row=0, column=1, padx=5, pady=3)
        #labelEntry.pack(side='right')

        self.EntryTest2 = tk.Entry(frameTest)
        self.EntryTest2.grid(row=1, column=1, padx=5, pady=3)        

        self.buttonTest = tk.Button(frameTest, text="Test", command=self.processButtonTest, bg='red')
        self.buttonTest.grid(row=2, column=2, padx=5, pady=3)

        self.scale = tk.Scale(frameTest, orient=tk.HORIZONTAL)
        self.scale.grid(row=2, column=1, sticky=tk.N+tk.W)

        # ==============================================================

        self.thread1 = threading.Thread(target=self.processUpdateData)
        self.thread1.start()

        self.window.mainloop()


    def processButtonSS(self):
        
        if (self.comState):
            if self.com_protocol.close_com_port() == True:
                self.comState = False
                self.buttonSS["text"] = "COM Open"

        else:
            if self.com_protocol.open_com_port() == True:
                self.comState = True
                self.buttonSS["text"] = "COM Close"


    def processButtonSend(self):
        if (self.comState):
            text = self.entrySpeed.get()
            val = int(text)
            b = int.to_bytes(val, length=2, byteorder='little', signed=True)

            btarray = bytearray(12)
            btarray[0] = int('5A', 16)
            btarray[1] = int('20', 16)
            btarray[2] = int(b[0])
            btarray[3] = int(b[1])
            btarray[11]= int('A5', 16)

            bytesToSend = bytes(btarray)
            print(bytesToSend)

            self.com_protocol.serial_port.write(bytesToSend)

        
    def processButtonMotorStart(self):
            btarray = bytearray(12)
            btarray[0] = int('5A', 16)
            btarray[1] = int('10', 16)
            btarray[11]= int('A5', 16)

            bytesToSend = bytes(btarray)
            print(bytesToSend)

            self.com_protocol.serial_port.write(bytesToSend)


    def processButtonMotorStop(self):
            btarray = bytearray(12)
            btarray[0] = int('5A', 16)
            btarray[1] = int('11', 16)
            btarray[11]= int('A5', 16)

            bytesToSend = bytes(btarray)
            print(bytesToSend)

            self.com_protocol.serial_port.write(bytesToSend)


    def processButtonScope(self):

        if (self.comState):
            if self.scope.enable == False:
                self.scope.start()

            if self.buttonScope["text"] == "Scope ON":
                self.buttonScope["text"] = "Scope OFF"
                cmd = '01'
            else:
                self.buttonScope["text"] = "Scope ON"
                cmd = '00'

            btarray = bytearray(12)
            btarray[0] = int('5A', 16)
            btarray[1] = int('10', 16)
            btarray[2] = int(cmd, 16)
            btarray[11]= int('A5', 16)

            bytesToSend = bytes(btarray)
            print(bytesToSend)

            self.com_protocol.serial_port.write(bytesToSend)


    def readFromSerialPort(self):
        data = []
        if (self.comState):
            data = self.com_protocol.read_from_data_buffer()

        return data


    def processButtonTest(self):
        self.labelTest['text'] = "Hello World"

        if (self.comState):
            btarray = bytearray(12)
            btarray[0] = int('5A', 16)
            btarray[1] = int('10', 16)
            btarray[2] = int('AA', 16)
            btarray[11]= int('A5', 16)

            bytesToSend = bytes(btarray)
            print(bytesToSend)

            self.com_protocol.serial_port.write(bytesToSend)

    def processUpdateData(self):

        while True:
            time.sleep(0.1)

            val = self.com_protocol.read_ptr
            self.EntryTest1['textvariable'] = tk.StringVar(value=str(val))

            val = self.com_protocol.write_idx
            self.EntryTest2['textvariable'] = tk.StringVar(value=str(val))

            for i in range(5):
                val = self.com_protocol.motor_info_buf[i]
                self.entryDebug[i]['textvariable'] = tk.IntVar(value=int(val))


if __name__ == '__main__':
    app = mainGUI()


