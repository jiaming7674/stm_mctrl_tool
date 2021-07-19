import numpy as np
import serial
import threading
import time


class COMPort():

    def __init__(self):
        self.serial_port = serial.Serial()
        self.serial_port.port = "COM4"
        self.serial_port.baudrate = 115200
        self.serial_port.parity = serial.PARITY_NONE
        self.serial_port.stopbits = serial.STOPBITS_ONE

        self.serial_port.timeout = 0.01  # sec

        self.com_status = False

        self.read_ptr = 0
        self.write_ptr = 0
        self.buf_size = 4096
        self.received_ch1_buf = np.zeros(self.buf_size)
        self.received_ch2_buf = np.zeros(self.buf_size)
        print("COM Port init. Done")


    def open(self):
        try:
            self.serial_port.open()
            print("COM Open")
            self.com_status = True
            self.thread = threading.Thread(target=self.readUART)
            self.thread.start()
        except:
            print("Can't open COM")

        return self.serial_port.is_open


    def close(self):
        try:
            self.com_status = False
            time.sleep(1)
            self.serial_port.close()
            print("COM Close")
        except:
            print("Error")

        if self.serial_port.is_open == False:
            return True
        else:
            return False


    def readUART(self):

        while self.com_status:
            try:
                ch = self.serial_port.read(4)

                if (len(ch) == 4):
                    d1 = int.from_bytes(ch[0:2], 'little', signed=True)
                    d2 = int.from_bytes(ch[2:], 'little', signed=True)
                    
                    data = []
                    data.append(d1)
                    data.append(d2)
                    
                    self.wirte_to_buffer(data)

                
            except:
                print("Error")


    def wirte_to_buffer(self, data):

        self.received_ch1_buf[self.write_ptr] = data[0]
        self.received_ch2_buf[self.write_ptr] = data[1]

        self.write_ptr += 1

        if self.write_ptr >= self.buf_size:
            self.write_ptr = 0


    def is_buffer_not_empty(self):

        d = self.write_ptr - self.read_ptr

        if d < 0:  d += self.buf_size

        if d != 0:
            return True
        else:
            return False


    def read_from_buffer(self):

        data = []

        data.append(self.received_ch1_buf[self.read_ptr])
        data.append(self.received_ch2_buf[self.read_ptr])

        self.read_ptr += 1

        if self.read_ptr >= self.buf_size:
            self.read_ptr = 0

        return data
