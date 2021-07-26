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

        num_of_channel = len(self.motorInfo.to_plot_data)
        self.scope2 = Scope(num_of_channels=num_of_channel, data_len=1000, fps=50)
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
        self.labelState = tk.Label(frameMotorInfo, text="State: ")
        self.entryState = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))
        self.labelError = tk.Label(frameMotorInfo, text="Error: ")
        self.entryError = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))

        self.labelSpeedRef = tk.Label(frameMotorInfo, text="Speed Ref: ")
        self.entrySpeedRef = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))
        self.labelSpeed = tk.Label(frameMotorInfo, text="Speed: ")
        self.entrySpeed = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))
        self.labelVBUS = tk.Label(frameMotorInfo, text="Bus Volt: ")
        self.entryVBUS = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))

        self.labelCurAmplitude = tk.Label(frameMotorInfo, text="Cur Amp: ")
        self.entryCurAmplitude = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))
        self.labelIsd = tk.Label(frameMotorInfo, text="Isd: ")
        self.entryIsd = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))
        self.labelIsq = tk.Label(frameMotorInfo, text="Isq: ")
        self.entryIsq = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))


        self.labelVoltAmplitude = tk.Label(frameMotorInfo, text="Volt Amp: ")
        self.entryVoltAmplitude = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))
        self.labelVdRef = tk.Label(frameMotorInfo, text="Vd Ref:")
        self.entryVdRef = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))
        self.labelVqRef = tk.Label(frameMotorInfo, text="Vq Ref:")
        self.entryVqRef = tk.Entry(frameMotorInfo, textvariable=tk.IntVar(value=0))

        self.buttonScope = tk.Button(frameMotorInfo, text="Scope ON", command=self.processButtonScope)


        self.labelConnection.grid(row=0, column=0, padx=5, pady=3, sticky=tk.W+tk.E+tk.S+tk.N)
        self.entryConnection.grid(row=0, column=1, padx=5, pady=3)
        self.labelState.grid(row=0, column=2, padx=5, pady=3)
        self.entryState.grid(row=0, column=3, padx=5, pady=3)
        self.labelError.grid(row=0, column=4, padx=5, pady=3)
        self.entryError.grid(row=0, column=5, padx=5, pady=3)
        self.labelSpeedRef.grid(row=1, column=0, padx=5, pady=3)
        self.entrySpeedRef.grid(row=1, column=1, padx=5, pady=3)
        self.labelSpeed.grid(row=1, column=2, padx=5, pady=3)
        self.entrySpeed.grid(row=1, column=3, padx=5, pady=3)
        self.labelVBUS.grid(row=1, column=4, padx=5, pady=3)
        self.entryVBUS.grid(row=1, column=5, padx=5, pady=3)
        self.labelCurAmplitude.grid(row=2, column=0, padx=5, pady=3)
        self.entryCurAmplitude.grid(row=2, column=1, padx=5, pady=3)
        self.labelIsd.grid(row=2, column=2, padx=5, pady=3)
        self.entryIsd.grid(row=2, column=3, padx=5, pady=3)
        self.labelIsq.grid(row=2, column=4, padx=5, pady=3)
        self.entryIsq.grid(row=2, column=5, padx=5, pady=3)

        self.labelVoltAmplitude.grid(row=3, column=0, padx=5, pady=3)
        self.entryVoltAmplitude.grid(row=3, column=1, padx=5, pady=3)
        self.labelVdRef.grid(row=3, column=2, padx=5, pady=3)
        self.entryVdRef.grid(row=3, column=3, padx=5, pady=3)
        self.labelVqRef.grid(row=3, column=4, padx=5, pady=3)
        self.entryVqRef.grid(row=3, column=5, padx=5, pady=3)        

        self.buttonScope.grid(row=4, column=5, padx=10, pady=10)

        # Control Frame ==================================================

        frameControl = tk.Frame(self.window)
        frameControl.grid(row=2, column=0, padx=5, pady=20)

        self.labelSetSpeed = tk.Label(frameControl, text="Set Speed: ")
        self.entrySetSpeed = tk.Entry(frameControl, textvariable=tk.IntVar(value='0'))
        self.buttonSetSpeed = tk.Button(frameControl, text="Set", command=self.processButtonSetSpeedSend, width = 10)

        self.labelSetCurRef = tk.Label(frameControl, text="Set Cur Ref: ")
        self.entrySetCurRef = tk.Entry(frameControl, textvariable=tk.IntVar(value='0'))
        self.buttonSetCurRef = tk.Button(frameControl, text="Set", command=self.processButtonSetCurRefSend, width = 10)

        self.buttonMotorStart = tk.Button(frameControl, text="Run", command=self.processButtonMotorStart, width = 10, bg='green')
        self.buttonMotorStop = tk.Button(frameControl, text="Stop", command=self.processButtonMotorStop, width = 10, bg='red')
        self.buttonFaultAck = tk.Button(frameControl, text="Fault Ack", command=self.processButtonFaultAck, width = 10)

        self.labelSetSpeed.grid(row=0, column=0, padx=5, pady=3)
        self.entrySetSpeed.grid(row=0, column=1, padx=5, pady=3)
        self.buttonSetSpeed.grid(row=0, column=2, padx=5, pady=3)
        self.buttonMotorStart.grid(row=0, column=3, padx=10, pady=3, sticky=tk.E)
        self.buttonMotorStop.grid(row=0, column=4, padx=10, pady=3, sticky=tk.E)
        self.buttonFaultAck.grid(row=0, column=5, padx=10, pady=3)

        self.labelSetCurRef.grid(row=1, column=0, padx=5, pady=3)
        self.entrySetCurRef.grid(row=1, column=1, padx=5, pady=3)
        self.buttonSetCurRef.grid(row=1, column=2, padx=5, pady=3)

        # Parameter Frame ==================================================

        frameParameter = tk.Frame(self.window)
        frameParameter.grid(row=3, column=0, padx=5, pady=20)

        self.labelSetRs = tk.Label(frameParameter, text="Rs: ")
        self.entrySetRs = tk.Entry(frameParameter, textvariable=tk.IntVar(value=0))
        self.buttonSetRs = tk.Button(frameParameter, text="Set", command=None)

        self.labelSetLs = tk.Label(frameParameter, text="Ls: ")
        self.entrySetLs = tk.Entry(frameParameter, textvariable=tk.IntVar(value=0))
        self.buttonSetLs = tk.Button(frameParameter, text="Set", command=None)

        self.labelSetlamaf = tk.Label(frameParameter, text="Lamaf: ")
        self.entrySetlamaf = tk.Entry(frameParameter, textvariable=tk.IntVar(value=0))
        self.buttonSetlamaf = tk.Button(frameParameter, text="Set", command=None)

        self.labelSetJs = tk.Label(frameParameter, text="Js: ")
        self.entrySetJs = tk.Entry(frameParameter, textvariable=tk.IntVar(value=0))
        self.buttonSetJs = tk.Button(frameParameter, text="Set", command=None)             

        self.labelSetBs = tk.Label(frameParameter, text="Bs: ")
        self.entrySetBs = tk.Entry(frameParameter, textvariable=tk.IntVar(value=0))
        self.buttonSetBs = tk.Button(frameParameter, text="Set", command=None)    

        self.labelSetRs.grid(row=0, column=0, padx=5, pady=3)
        self.entrySetRs.grid(row=0, column=1, padx=5, pady=3)
        self.buttonSetRs.grid(row=0, column=2, padx=5, pady=3)

        self.labelSetLs.grid(row=0, column=3, padx=5, pady=3)
        self.entrySetLs.grid(row=0, column=4, padx=5, pady=3)
        self.buttonSetLs.grid(row=0, column=5, padx=5, pady=3)

        self.labelSetlamaf.grid(row=0, column=6, padx=5, pady=3)
        self.entrySetlamaf.grid(row=0, column=7, padx=5, pady=3)
        self.buttonSetlamaf.grid(row=0, column=8, padx=5, pady=3)

        self.labelSetJs.grid(row=1, column=0, padx=5, pady=3)
        self.entrySetJs.grid(row=1, column=1, padx=5, pady=3)
        self.buttonSetJs.grid(row=1, column=2, padx=5, pady=3)

        self.labelSetBs.grid(row=1, column=3, padx=5, pady=3)
        self.entrySetBs.grid(row=1, column=4, padx=5, pady=3)
        self.buttonSetBs.grid(row=1, column=5, padx=5, pady=3)

        # Debug Frame ==================================================
        frameDebug = tk.Frame(self.window)
        frameDebug.grid(row=4, column=0)

        self.labelDebug = []
        self.entryDebug = []

        for i in range(6):
            self.labelDebug.append(tk.Label(frameDebug, text='D'+ str(i) + ': '))
            self.entryDebug.append(tk.Entry(frameDebug, textvariable=tk.IntVar(value=0)))

            self.labelDebug[i].grid(row=i, column=0, padx=5, pady=3)
            self.entryDebug[i].grid(row=i, column=1, padx=5, pady=3)


        # Test Frame ==================================================

        frameTest = tk.Frame(self.window)
        frameTest.grid(row=5, column=0)

        self.labelTest = tk.Label(frameTest, text="Test : ", bg='yellow')
        self.labelTest.grid(row=0, column=0, padx=5, pady=3)
        #labelTest.pack(side='left')

        self.EntryTest1 = tk.Entry(frameTest)
        self.EntryTest1.grid(row=0, column=1, padx=5, pady=3)
        #labelEntry.pack(side='right')

        self.EntryTest2 = tk.Entry(frameTest)
        self.EntryTest2.grid(row=0, column=2, padx=5, pady=3)        

        self.buttonTest = tk.Button(frameTest, text="Test", command=self.processButtonTest, bg='red')
        self.buttonTest.grid(row=0, column=3, padx=5, pady=3)


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


    def processButtonSetSpeedSend(self):
        if (self.comState):
            text = self.entrySetSpeed.get()
            val = float(text)
            val = int(val / 60 * 10)
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


    def processButtonSetCurRefSend(self):
        if (self.comState):
            text = self.entrySetCurRef.get()
            val = int(text)
            b = int.to_bytes(val, length=2, byteorder='little', signed=True)

            btarray = bytearray(12)
            btarray[0] = int('5A', 16)
            btarray[1] = int('30', 16)
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


    def processButtonFaultAck(self):
        if (self.comState):
            btarray = bytearray(12)
            btarray[0] = int('5A', 16)
            btarray[1] = int('12', 16)
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
            for i in range(len(self.motorInfo.to_plot_data)):
                d.append(self.motorInfo.to_plot_data[i])
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

            for i in range(len(self.motorInfo.to_plot_data_ylim)):
                self.scope2.set_channel_ylim(i, self.motorInfo.to_plot_data_ylim[i])

            # Update Motor State
            val = self.motorInfo.get_motor_state()
            self.entryState['textvariable'] = tk.StringVar(value=val)

            # Update Motor Speed
            val = self.motorInfo.motor_spd_ref_rpm
            self.entrySpeedRef['textvariable'] = tk.StringVar(value=str(val) + ' rpm')

            val = self.motorInfo.motor_speed_rpm
            self.entrySpeed['textvariable'] = tk.StringVar(value=str(val) + ' rpm')

            # Update Motor Current Information
            val = self.motorInfo.cur_amplitude
            self.entryCurAmplitude['textvariable'] = tk.StringVar(value=str(val))

            val = self.motorInfo.isd_ref
            

            # Update Motor Voltage Command
            val = self.motorInfo.volt_amplitude
            self.entryVoltAmplitude['textvariable'] = tk.StringVar(value=str(val))

            val = self.motorInfo.vd_ref
            self.entryVdRef['textvariable'] = tk.StringVar(value=str(val))

            val = self.motorInfo.vq_ref
            self.entryVqRef['textvariable'] = tk.StringVar(value=str(val))            


            for i in range(len(self.entryDebug)):
                val = self.com_protocol.motor_info_buf[i + 11]
                self.entryDebug[i]['textvariable'] = tk.IntVar(value=int(val))


if __name__ == '__main__':
    app = mainGUI()



