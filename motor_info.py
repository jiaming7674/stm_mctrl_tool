import numpy as np

class MotorInfo():

    def __init__(self):

        self.motor_state = 0
        self.fault_state = 0
        self.motor_spd_ref_rpm = 0
        self.motor_speed_rpm = 0
        self.bus_voltage = 0

        self.isd_ref = 0
        self.isq_ref = 0

        self.isd = 0
        self.isq = 0

        self.cur_amplitude = 0
        self.volt_amplitude = 0

        self.vd_ref = 0
        self.vq_ref = 0

        self.plot_data = [
            {'d' : self.motor_spd_ref_rpm, 'ylim' : [-2000, 14000], 'label' : 'speed_ref', 'channel' : 0},
            {'d' : self.motor_speed_rpm, 'ylim' : [-2000, 14000], 'label' : 'speed', 'channel' : 0},
            {'d' : self.vd_ref, 'ylim' : [-10000, 1000], 'label' : 'vd_ref', 'channel' : 1},
            {'d' : self.vq_ref, 'ylim' : [-1000, 40000], 'label' : 'vq_ref', 'channel' : 2},
            {'d' : self.cur_amplitude, 'ylim' : [-1000, 1500], 'label' : 'vq_ref', 'channel' : 3},
        ]

        
    def update_motor_info(self, motor_info_buf):

        self.motor_state = int(motor_info_buf[0])
        self.fault_state = int(motor_info_buf[1])
        self.motor_spd_ref_rpm = int(motor_info_buf[2] * 60 / 10)
        self.motor_speed_rpm = int(motor_info_buf[3] * 60 / 10)

        self.cur_amplitude = int(motor_info_buf[5])
        self.isd = int(motor_info_buf[7])
        self.isq = int(motor_info_buf[8])

        self.volt_amplitude = int(motor_info_buf[6])
        self.vd_ref = int(motor_info_buf[9])
        self.vq_ref = int(motor_info_buf[10])

        self.plot_data[0]['d'] = self.motor_spd_ref_rpm
        self.plot_data[1]['d'] = self.motor_speed_rpm
        self.plot_data[2]['d'] = self.vd_ref
        self.plot_data[3]['d'] = self.vq_ref
        self.plot_data[4]['d'] = self.cur_amplitude


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

