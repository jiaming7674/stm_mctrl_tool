import numpy as np
import serial
import threading
import time


class CommunicationProtocol():

    def __init__(self):

        self.serial_port = serial.Serial()
        self.serial_port.port = "COM4"
        self.serial_port.baudrate = 115200
        self.serial_port.parity = serial.PARITY_NONE
        self.serial_port.stopbits = serial.STOPBITS_ONE
        self.serial_port.timeout = 100  # sec

        self.com_status = False

        self.recv_bytes_buf_size = 1024
        self.received_bytes_buf = bytearray(self.recv_bytes_buf_size)
        self.write_ptr = 0
        self.read_ptr = 0

        self.num_channel = 2
        self.data_buf_size = 128
        self.received_data_buf = []

        self.frame_size = 6 + 2 * self.num_channel

        self.read_idx = 0
        self.write_idx = 0

        for _ in range(self.num_channel):
            self.received_data_buf.append(np.zeros(self.data_buf_size))

        self.motor_info_buf = np.zeros(256)


    def open_com_port(self):
        '''This method is used to open the serial port.'''
        try:
            self.serial_port.open()
            print("COM Open")
            self.com_status = True
            self.thread1 = threading.Thread(target=self.read_from_serial_port)
            self.thread1.start()

            self.thread2 = threading.Thread(target=self.read_from_received_bytes_buffer)
            self.thread2.start()
        except:
            print("Can't open COM")

        return self.serial_port.is_open


    def close_com_port(self):
        '''This method is used to close the serial com port.'''
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


    def read_from_serial_port(self):
        '''It reads a few bytes from serial port and stores bytes to the received buffer.
           This method is executed by created thread.'''
        while self.com_status == True:
            try:
                ch = self.serial_port.read(6)

                for i in range(len(ch)):
                    self.received_bytes_buf[self.write_ptr] = ch[i]
                    self.write_ptr += 1

                    if self.write_ptr >= self.recv_bytes_buf_size:
                        self.write_ptr = 0

            except:
                print("Error r01")


    def bytes_to_read(self):
        '''Get how many bytes can be read.'''
        d = self.write_ptr - self.read_ptr
        if d < 0: d += self.recv_bytes_buf_size

        return d


    def buffer_empty(self):
        d = self.bytes_to_read()
        return d == 0


    def read_from_received_bytes_buffer(self):

        while self.com_status:
            
            if self.bytes_to_read() >= self.frame_size:
                frame_bytes = bytearray(self.frame_size)

                for i in range(self.frame_size):
                    ptr = self.read_ptr + i
                    if ptr >= self.recv_bytes_buf_size:
                        ptr -= self.recv_bytes_buf_size
                    frame_bytes[i] = self.received_bytes_buf[ptr]

                if frame_bytes[0] == int('5A', 16) and frame_bytes[self.frame_size-1] == int('A5', 16):
                    self.read_ptr += self.frame_size

                    index = frame_bytes[1]

                    self.motor_info_buf[index] = int.from_bytes(frame_bytes[2:4], byteorder='little', signed=True)

                    if self.read_ptr >= self.recv_bytes_buf_size:
                        self.read_ptr -= self.recv_bytes_buf_size

                    for j in range(self.num_channel):
                        self.received_data_buf[j][self.write_idx] = int.from_bytes(frame_bytes[j*2+4:j*2+6], 'little', signed=True)

                    self.write_idx += 1
                    if self.write_idx >= self.data_buf_size:
                        self.write_idx = 0

                else:
                    self.read_ptr += 1
                    if self.read_ptr >= self.recv_bytes_buf_size:
                        self.read_ptr = 0

            else:
                time.sleep(0.005)


    def datas_to_read(self):
        d = self.write_idx - self.read_idx
        if d < 0: d += self.data_buf_size
        return d

    
    def read_from_data_buffer(self):
        '''Read received data from data buffer.'''
        data = []

        while self.datas_to_read():
            ng = []

            for i in range(self.num_channel):
                ng.append(self.received_data_buf[i][self.read_idx])

            self.read_idx += 1
            if self.read_idx >= self.data_buf_size:
                self.read_idx = 0

            data.append(ng)

        return data
