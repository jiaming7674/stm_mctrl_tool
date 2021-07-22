import numpy as np

class MotorInfo():

    def __init__(self):

        self.motor_state = 0
        self.motor_speed_rpm = 0
        self.bus_voltage = 0

        
    def update_motor_info(self, motor_info_buf):

        self.motor_speed_rpm = motor_info_buf[2] * 60 / 10