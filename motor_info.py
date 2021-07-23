import numpy as np

class MotorInfo():

    def __init__(self):

        self.motor_state = 0
        self.fault_state = 0
        self.motor_speed_rpm = 0
        self.bus_voltage = 0

        self.isd_ref = 0
        self.isq_ref = 0

        self.cur_amplitude = 0
        self.volt_amplitude = 0

        self.vd_ref = 0
        self.vq_ref = 0

        self.to_plot_data_ylim = [
                            [0, 14000],
                            [-50000, 50000],
                            [-50000, 50000],
        ]

        self.to_plot_data = [self.motor_speed_rpm,
                             self.vd_ref,
                             self.vq_ref]

        
    def update_motor_info(self, motor_info_buf):

        self.motor_state = int(motor_info_buf[0])
        self.fault_state = motor_info_buf[1]
        self.motor_speed_rpm = motor_info_buf[3] * 60 / 10

        self.volt_amplitude = int(motor_info_buf[6])
        self.vd_ref = int(motor_info_buf[9])
        self.vq_ref = int(motor_info_buf[10])

        self.to_plot_data = [self.motor_speed_rpm,
                             self.vd_ref,
                             self.vq_ref]


    def get_motor_state(self):

        state = 'UNKNOW'

        try:
            state_arr = ['IDLE', 
                        'IDLE_ALIGNMENT',
                        'ALIGNMENT',
                        'IDLE_START',
                        'START',
                        'START_RUN',
                        'RUN',
                        'ANY_STOP',
                        'STOP',
                        'STOP_IDLE',
                        'FAULT_NOW',
                        'FAULT_OVER',
                        ]

            state = state_arr[self.motor_state]
        
        except:
            return state

        return state

