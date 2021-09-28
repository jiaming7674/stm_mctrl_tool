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
        self.monitorState = False
        self.isRunning = True

        self.com_protocol = CommunicationProtocol()
        self.motorInfo = MotorInfo()

        self.scope1 = Scope(data_len=1600, fps=10)
        self.scope1.callback = self.readFromSerialPort

        self.scope1.set_channel_ylim(0, [-10000, 10000])
        self.scope1.set_channel_ylim(1, [-40000, 40000])

        self.scope2 = Scope(num_of_channels=4, data_len=1000, fps=50, plot_data=self.motorInfo.plot_data)
        self.scope2.callback = self.readFromMotorInfo

        for i in range(len(self.motorInfo.plot_data)):
            ch = self.motorInfo.plot_data[i]['channel']
            self.scope2.set_channel_ylim(ch, self.motorInfo.plot_data[i]['ylim'])

        # COM Information Frame =====================================
        frame_COMinf = tk.Frame(self.window)
        frame_COMinf.grid(row=0, column=0)

        self.labelCOM = tk.Label(frame_COMinf, text="COMx: ")
        self.COM = tk.StringVar(value="COM3")
        self.entryCOM = tk.Entry(frame_COMinf, textvariable=self.COM)

        self.labelBaudrate = tk.Label(frame_COMinf, text="Baudrate: ")
        self.Baudrate = tk.IntVar(value=921600)
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
        self.buttonMonitorON = tk.Button(frame_COMinf, text="Monitor ON", command=self.processButtonMonitorON)
        self.buttonMonitorOFF = tk.Button(frame_COMinf, text="Monitor OFF", command=self.processButtonMonitorOFF)

        self.labelCOM.grid(row=0, column=0, padx=5, pady=3)
        self.entryCOM.grid(row=0, column=1, padx=5, pady=3)
        self.labelBaudrate.grid(row=0, column=2, padx=5, pady=3)
        self.entryBaudrate.grid(row=0, column=3, padx=5, pady=3)
        self.labelParity.grid(row=1, column=0, padx=5, pady=3)
        self.comboParity.grid(row=1, column=1, padx=5, pady=3)
        self.labelStopbits.grid(row=1, column=2, padx=5, pady=3)
        self.comboStopbits.grid(row=1, column=3, padx=5, pady=3)
        self.buttonSS.grid(row=1, column=4, padx=5, pady=3)
        self.buttonMonitorON.grid(row=1, column=5, padx=5, pady=3)
        self.buttonMonitorOFF.grid(row=1, column=6, padx=5, pady=3)

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
        self.entrySetRs = tk.Entry(frameParameter, textvariable=tk.IntVar(value=0.2))
        self.buttonSetRs = tk.Button(frameParameter, text="Set", command=self.processButtonSetRs)

        self.labelSetLs = tk.Label(frameParameter, text="Ls: ")
        self.entrySetLs = tk.Entry(frameParameter, textvariable=tk.IntVar(value=0.001))
        self.buttonSetLs = tk.Button(frameParameter, text="Set", command=self.processButtonSetLs)

        self.labelSetlamaf = tk.Label(frameParameter, text="Lamaf: ")
        self.entrySetlamaf = tk.Entry(frameParameter, textvariable=tk.IntVar(value=0.0016))
        self.buttonSetlamaf = tk.Button(frameParameter, text="Set", command=self.processButtonSetLamaf)

        self.labelSetJs = tk.Label(frameParameter, text="Js: ")
        self.entrySetJs = tk.Entry(frameParameter, textvariable=tk.IntVar(value=0.000008))
        self.buttonSetJs = tk.Button(frameParameter, text="Set", command=self.processButtonSetMecParm)             

        self.labelSetBs = tk.Label(frameParameter, text="Bs: ")
        self.entrySetBs = tk.Entry(frameParameter, textvariable=tk.IntVar(value=0.000004))
        self.buttonSetBs = tk.Button(frameParameter, text="Set", command=self.processButtonSetMecParm)    

        self.labelSetPhiGain = tk.Label(frameParameter, text="PhiGain: ")
        self.entrySetPhiGain = tk.Entry(frameParameter, textvariable=tk.IntVar(value=0))
        self.buttonSetPhiGain = tk.Button(frameParameter, text="Set", command=self.processButtonSetPhiGain)

        self.labelSetCompDGain = tk.Label(frameParameter, text="CompDGain: ")
        self.entrySetCompDGain = tk.Entry(frameParameter, textvariable=tk.IntVar(value=0.1))
        self.buttonSetCompDGain = tk.Button(frameParameter, text="Set", command=self.processButtonSetComdDGain)

        self.labelSetCompQGain = tk.Label(frameParameter, text="CompQGain: ")
        self.entrySetCompQGain = tk.Entry(frameParameter, textvariable=tk.IntVar(value=0.1))
        self.buttonSetCompQGain = tk.Button(frameParameter, text="Set", command=self.processButtonSetComdQGain)

        self.labelSetCompShift = tk.Label(frameParameter, text="CompPhaseShift: ")
        self.entrySetCompShift = tk.Entry(frameParameter, textvariable=tk.IntVar(value=60))
        self.buttonSetCompShift = tk.Button(frameParameter, text="Set", command=self.processButtonSetCompPhaseShift)                

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

        self.labelSetPhiGain.grid(row=2, column=0, padx=5, pady=3)
        self.entrySetPhiGain.grid(row=2, column=1, padx=5, pady=3)
        self.buttonSetPhiGain.grid(row=2, column=2, padx=5, pady=3)

        self.labelSetCompDGain.grid(row=3, column=0, padx=5, pady=3)
        self.entrySetCompDGain.grid(row=3, column=1, padx=5, pady=3)
        self.buttonSetCompDGain.grid(row=3, column=2, padx=5, pady=3)

        self.labelSetCompQGain.grid(row=3, column=3, padx=5, pady=3)
        self.entrySetCompQGain.grid(row=3, column=4, padx=5, pady=3)
        self.buttonSetCompQGain.grid(row=3, column=5, padx=5, pady=3)

        self.labelSetCompShift.grid(row=3, column=6, padx=5, pady=3)
        self.entrySetCompShift.grid(row=3, column=7, padx=5, pady=3)
        self.buttonSetCompShift.grid(row=3, column=8, padx=5, pady=3)

        # Debug Frame ==================================================
        frameDebug = tk.Frame(self.window)
        frameDebug.grid(row=4, column=0)

        self.labelDebug = []
        self.entryDebug = []

        for i in range(6):
            self.labelDebug.append(tk.Label(frameDebug, text='D'+ str(i+1) + ': '))
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

        self.EntryTest3 = tk.Entry(frameTest)
        self.EntryTest3.grid(row=1, column=0, padx=5, pady=3)            

        self.buttonTest = tk.Button(frameTest, text="Test", command=self.processButtonTest, bg='red')
        self.buttonTest.grid(row=0, column=3, padx=5, pady=3)


    def start(self):
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


    def processButtonMonitorON(self):
        self.send_tx_frame(int('71', 16), 0)

    def processButtonMonitorOFF(self):
        self.send_tx_frame(int('70', 16), 0)


    def processButtonSetSpeedSend(self):
        if (self.comState):
            text = self.entrySetSpeed.get()
            val = float(text)
            val = int(val / 60 * 10)
            self.send_tx_frame(int('20', 16), val)


    def processButtonSetCurRefSend(self):
        val = int(float(self.entrySetCurRef.get()) * 7342)
        self.send_tx_frame(int('30', 16), val)

        
    def processButtonMotorStart(self):
        self.send_tx_frame(int('10', 16), 0)


    def processButtonMotorStop(self):
        self.send_tx_frame(int('11', 16), 0)


    def processButtonFaultAck(self):
        self.send_tx_frame(int('12', 16), 0)


    def processButtonSetRs(self):
        try:
            text = self.entrySetRs.get()
            val = float(text)
            val = int(val*65535)
            print(val)
            self.send_tx_frame(int('40', 16), val, signed=False)
        except Exception as e:
            print(e)


    def processButtonSetLs(self):
        try:
            text = self.entrySetLs.get()
            val = float(text)
            val = int(val*65535)
            self.send_tx_frame(int('41', 16), val, signed=False)
        except Exception as e:
            print(e)

    def processButtonSetLamaf(self):
        try:
            text = self.entrySetlamaf.get()
            val = float(text)
            val = int(val*65535)
            self.send_tx_frame(int('42', 16), val, signed=False)
        except Exception as e:
            print(e)

    def processButtonSetMecParm(self):
        try:
            J = float(self.entrySetJs.get())
            B = float(self.entrySetBs.get())
            Ts = 1/32e3

            val1 = int(Ts/J * 16777216)
            b1 = val1.to_bytes(4, 'little', signed=True)
            self.send_tx_frame(int('43', 16), int.from_bytes(b1[0:2], 'little', signed=False), signed=False)
            time.sleep(0.1)
            self.send_tx_frame(int('44', 16), int.from_bytes(b1[2:4], 'little', signed=False), signed=False)
            time.sleep(0.1)

            val2 = int(1/(1+B/J*Ts) * 16777216)
            b2 = val2.to_bytes(4, 'little', signed=True)
            self.send_tx_frame(int('45', 16), int.from_bytes(b2[0:2], 'little', signed=False), signed=False)
            time.sleep(0.1)
            self.send_tx_frame(int('46', 16), int.from_bytes(b2[2:4], 'little', signed=False), signed=False)
            self.send_tx_frame(int('47', 16), 0)
        except Exception as e:
            print(e)


    def processButtonSetPhiGain(self):
        try:
            val = int(self.entrySetPhiGain.get())
            self.send_tx_frame(int('48', 16), val, signed=True)
        except Exception as e:
            print(e)


    def processButtonSetComdDGain(self):
        try:
            val = int(float(self.entrySetCompDGain.get()) * 32768)
            self.send_tx_frame(int('60', 16), val, signed=True)
        except Exception as e:
            print(e)


    def processButtonSetComdQGain(self):
        try:
            val = int(float(self.entrySetCompQGain.get()) * 32768)
            self.send_tx_frame(int('61', 16), val, signed=True)
        except Exception as e:
            print(e)


    def processButtonSetCompPhaseShift(self):
        try:
            val = int(float(self.entrySetCompShift.get()) / 180 * 32768)
            self.send_tx_frame(int('62', 16), val, signed=True)
        except Exception as e:
            print(e)


    def send_tx_frame(self, code, data, signed=True):
        if (self.comState):
            b = data.to_bytes(2, 'little', signed=signed)

            btarray = bytearray(12)
            btarray[0] = int('5A', 16)
            btarray[1] = code
            btarray[2] = b[0]
            btarray[3] = b[1]
            btarray[11] = int('5A', 16)

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

        if (self.comState):

            read_num = self.com_protocol.datas_to_read()
            data = np.zeros((2, read_num))

            read_idx = self.com_protocol.read_idx
            buf_size = self.com_protocol.data_buf_size

            for i in range(read_num):
                data[0][i] = self.com_protocol.received_data_buf[0][read_idx]
                data[1][i] = self.com_protocol.received_data_buf[1][read_idx]

                read_idx += 1
                if read_idx >= buf_size:
                    read_idx = 0
            
            self.com_protocol.read_idx = read_idx

            return data

        else:
            return np.zeros((2, 0))

    
    def readFromMotorInfo(self):

        if (self.comState):
            num_of_data = len(self.motorInfo.plot_data)
            data = np.zeros((num_of_data, 1))

            for i in range(len(self.motorInfo.plot_data)):
                data[i][0] = self.motorInfo.plot_data[i]['d']

            return data

        else:
            num_of_data = len(self.motorInfo.plot_data)
            return np.zeros((num_of_data,0))


    def processButtonTest(self):
        self.labelTest['text'] = "Hello World"


    def processUpdateData(self):

        while self.isRunning == True:
            time.sleep(0.1)

            self.motorInfo.update_motor_info(self.com_protocol.motor_info_buf)

            val = self.com_protocol.read_ptr
            self.EntryTest1['textvariable'] = tk.StringVar(value=str(val))

            val = self.com_protocol.write_idx
            self.EntryTest2['textvariable'] = tk.StringVar(value=str(val))

            val = self.com_protocol.data_num
            self.EntryTest3['textvariable'] = tk.StringVar(value=str(val))
            

            # Update Motor State
            val = self.motorInfo.get_motor_state()
            self.entryState['textvariable'] = tk.StringVar(value=val)

            val = self.motorInfo.fault_state
            val = str(val)
            self.entryError['textvariable'] = tk.StringVar(value=val)

            # Update Motor Speed
            val = self.motorInfo.motor_spd_ref_rpm
            self.entrySpeedRef['textvariable'] = tk.StringVar(value=str(val) + ' rpm')

            val = self.motorInfo.motor_speed_rpm
            self.entrySpeed['textvariable'] = tk.StringVar(value=str(val) + ' rpm')

            # Update Motor Current Information
            val = self.motorInfo.cur_amplitude
            self.entryCurAmplitude['textvariable'] = tk.StringVar(value=str(val))

            val = self.motorInfo.isd
            self.entryIsd['textvariable'] = tk.StringVar(value=str(val))

            val = self.motorInfo.isq
            self.entryIsq['textvariable'] = tk.StringVar(value=str(val))
            
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


    def quit(self):
        self.isRunning = False
        self.scope1.quit()
        self.scope2.quit()
        self.com_protocol.close_com_port()
        self.thread1.join()


if __name__ == '__main__':
    
    app = mainGUI()

    try:
        app.start()
    except:
        app.quit()
        print("quit ..")



