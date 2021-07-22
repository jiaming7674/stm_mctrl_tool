import numpy as np
import tkinter as tk
from tkinter import ttk
import threading
from communication_protocol import CommunicationProtocol
from scope import Scope
from motor_info import MotorInfo

import time
import threading

class mainGUI():

    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Motor Tool")

        self.comState = False

        self.com_protocol = CommunicationProtocol()
        self.motorInfo = MotorInfo()

        self.scope1 = Scope()
        self.scope1.callback = self.readFromSerialPort

        self.scope2 = Scope(num_of_channels=2, data_len=1000, fps=50)
        self.scope2.callback = self.readFromMotorInfo


        # COM Information Frame =====================================
        frame_COMinf = tk.Frame(self.window)
        frame_COMinf.grid(row=0, column=0)

        self.labelCOM = tk.Label(frame_COMinf, text="COMx: ")
        self.COM = tk.StringVar(value="COM4")
        self.entryCOM = tk.Entry(frame_COMinf, textvariable=self.COM)

        self.labelBaudrate = tk.Label(frame_COMinf, text="Baudrate: ")
        self.Baudrate = tk.IntVar(value=115200)
        self.entryBaudrate = tk.Entry(frame_COMinf, textvariable=self.Baudrate)

        self.labelParity = tk.Label(frame_COMinf, text="Parity: ")
        self.Parity = tk.StringVar(value="NONE")
        self.comboParity = ttk.Combobox(frame_COMinf, width=17, textvariable=self.Parity)
        self.comboParity["values"] = ("NONE","ODD","EVEN","MARK","SPACE")
        self.comboParity["state"] = "readonly"

        self.labelStopbits = tk.Label(frame_COMinf, text="Stopbits: ")
        self.Stopbits = tk.StringVar(value="1")
        self.comboStopbits = ttk.Combobox(frame_COMinf, width=17, textvariable=self.Stopbits)
        self.comboStopbits["values"] = ("1", "1.5", "2")
        self.comboStopbits["state"] = "readonly"
        self.buttonSS = tk.Button(frame_COMinf, text="COM Open", command=self.processButtonSS)

        self.labelCOM.grid(row=0, column=0, padx=5, pady=3)
        self.entryCOM.grid(row=0, column=1, padx=5, pady=3)
        self.labelBaudrate.grid(row=0, column=2, padx=5, pady=3)
        self.entryBaudrate.grid(row=0, column=3, padx=5, pady=3)
        self.labelParity.grid(row=1, column=0, padx=5, pady=3)
        self.comboParity.grid(row=1, column=1, padx=5, pady=3)
        self.labelStopbits.grid(row=1, column=2, padx=5, pady=3)
        self.comboStopbits.grid(row=1, column=3, padx=5, pady=3)
        self.buttonSS.grid(row=1, column=4, padx=5, pady=3)

        # Motor Information Frame =====================================
        frameMotorInfo = tk.Frame(self.window)
        frameMotorInfo.grid(row=1, column=0, padx=5, pady=10)

        self.labelConnection = tk.Label(frameMotorInfo, text="Connection: ")
        self.entryConnection = tk.Entry(frameMotorInfo, textvariable=tk.StringVar(value='Not Connected'))
        self.labelStatus = tk.Label(frameMotorInfo, text="Status: ")
        self.entryStatus = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))
        self.labelError = tk.Label(frameMotorInfo, text="Error: ")
        self.entryError = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))

        self.labelSpeed = tk.Label(frameMotorInfo, text="Speed: ")
        self.entrySpeed = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))


        self.labelConnection.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W+tk.E+tk.S+tk.N)
        self.entryConnection.grid(row=0, column=1, padx=5, pady=3)
        self.labelStatus.grid(row=0, column=2, padx=5, pady=3)
        self.entryStatus.grid(row=0, column=3, padx=5, pady=3)
        self.labelError.grid(row=0, column=4, padx=5, pady=3)
        self.entryError.grid(row=0, column=5, padx=5, pady=3)
        self.labelSpeed.grid(row=1, column=0, padx=5, pady=3)
        self.entrySpeed.grid(row=1, column=1, padx=5, pady=3)

        # Control Frame ==================================================

        frameControl = tk.Frame(self.window)
        frameControl.grid(row=2, column=0, padx=5, pady=20)

        self.labelSetSpeed = tk.Label(frameControl, text="Set Speed: ")
        self.entrySetSpeed = tk.Entry(frameControl, textvariable=tk.IntVar(value='0'))

        self.buttonSetSpeed = tk.Button(frameControl, text="Set", command=self.processButtonSend, width = 10)
        self.buttonMotorStart = tk.Button(frameControl, text="Run", command=self.processButtonMotorStart, width = 10, bg='green')
        self.buttonMotorStop = tk.Button(frameControl, text="Stop", command=self.processButtonMotorStop, width = 10, bg='red')

        self.labelSetSpeed.grid(row=0, column=0, padx=5, pady=3)
        self.entrySetSpeed.grid(row=0, column=1, padx=5, pady=3)
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

        for i in range(6):
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
        self.EntryTest1.grid(row=0, column=0, padx=5, pady=3)
        #labelEntry.pack(side='right')

        self.EntryTest2 = tk.Entry(frameTest)
        self.EntryTest2.grid(row=0, column=1, padx=5, pady=3)        

        self.buttonTest = tk.Button(frameTest, text="Test", command=self.processButtonTest, bg='red')
        self.buttonTest.grid(row=0, column=2, padx=5, pady=3)


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
            text = self.entrySetSpeed.get()
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

        if (self.comState):
            btarray = bytearray(12)
            btarray[0] = int('5A', 16)
            btarray[1] = int('10', 16)
            btarray[11]= int('A5', 16)

            bytesToSend = bytes(btarray)
            print(bytesToSend)

            self.com_protocol.serial_port.write(bytesToSend)


    def processButtonMotorStop(self):

        if (self.comState):
            btarray = bytearray(12)
            btarray[0] = int('5A', 16)
            btarray[1] = int('11', 16)
            btarray[11]= int('A5', 16)

            bytesToSend = bytes(btarray)
            print(bytesToSend)

            self.com_protocol.serial_port.write(bytesToSend)


    def processButtonScope(self):

        if (self.comState):
            if self.scope1.enable == False:
                self.scope1.start()

            if self.scope2.enable == False:
                self.scope2.start(plt_show=True)


    def readFromSerialPort(self):
        data = []
        if (self.comState):
            data = self.com_protocol.read_from_data_buffer()

        return data

    
    def readFromMotorInfo(self):
        data = []

        if (self.comState):
            d = []
            # d.append(self.com_protocol.motor_info_buf[2])
            d.append(self.motorInfo.motor_speed_rpm)
            d.append(self.com_protocol.motor_info_buf[3])

            data.append(d)

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

            self.motorInfo.update_motor_info(self.com_protocol.motor_info_buf)

            val = self.com_protocol.read_ptr
            self.EntryTest1['textvariable'] = tk.StringVar(value=str(val))

            val = self.com_protocol.write_idx
            self.EntryTest2['textvariable'] = tk.StringVar(value=str(val))


            self.scope2.set_channel_ylim(0, [0, 10000])

            # Update Motor Speed
            #val = self.com_protocol.motor_info_buf[2] * 60 / 10
            val = self.motorInfo.motor_speed_rpm
            self.entrySpeed['textvariable'] = tk.StringVar(value=str(int(val)) + ' rpm')


            for i in range(len(self.entryDebug)):
                val = self.com_protocol.motor_info_buf[i]
                self.entryDebug[i]['textvariable'] = tk.IntVar(value=int(val))


if __name__ == '__main__':
    app = mainGUI()


