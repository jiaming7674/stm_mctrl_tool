import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Scope():

    def __init__(self, num_of_channels=2, data_len=1000, fps=50, plot_data=None):

        self.enable = False

        self.num_of_channels=num_of_channels
        self.data_len = data_len
        self.fps = fps
        self.plot_data = plot_data

        self.fig, self.ax = plt.subplots(self.num_of_channels, 1, figsize=(10, 7), sharex='all')
        self.fig.subplots_adjust(top = 0.98, bottom = 0.05, left = 0.08, right = 0.95)

        self.lines = []

        self.x = np.arange(0, self.data_len, 1)
        self.y = []

        self.callback = self.null_func

        self.c = ['blue', 'red', 'green', 'orange', 'black']

        self.legends = []

        if self.plot_data == None:
            num_of_lines = num_of_channels
        else:
            num_of_lines = len(plot_data)

        for i in range(num_of_lines):
            line = plt.Line2D(self.x , np.zeros(len(self.x)), color=self.c[i])
            self.lines.append(line)

        for i in range(len(self.ax)):
            self.ax[i].set_xlim([0, self.data_len])
            self.ax[i].set_ylim([-40000, 40000])
            self.ax[i].grid()


    def set_channel_ylim(self, channel, ylim):
        self.ax[channel].set_ylim(ylim)


    def plot_init(self):

        for i in range(len(self.lines)):
            self.y.append(np.zeros(len(self.x)))
            self.lines[i].set_ydata(self.y[i])

        if self.plot_data == None:
            for i in range(len(self.lines)):
                self.ax[i].add_line(self.lines[i])   ### <<<<----
        else:
            for i in range(len(self.plot_data)):
                ch = self.plot_data[i]['channel']
                print('ch = %d, i=%d' % (ch, i))
                self.ax[ch].add_line(self.lines[i])


        return self.lines


    def animate(self, frame):

        data = self.callback()

        if data.shape[1] == 0:
            return self.lines

        # for i in range(len(data)):

        #     for j in range(len(self.lines)):
        #         self.y[j][0] = data[i][j]
        #         self.y[j] = np.roll(self.y[j], -1)

        # for i in range(len(self.lines)):
        #     self.lines[i].set_ydata(self.y[i])

        for i in range(data.shape[1]):
            for j in range(data.shape[0]):
                self.y[j][0] = data[j][i]
                self.y[j] = np.roll(self.y[j], -1)

        for i in range(len(self.lines)):
            self.lines[i].set_ydata(self.y[i])

        return self.lines


    def start(self, plt_show=False):

        self.enable = True

        interval = int(1/self.fps * 1000)

        print(interval)

        self.ani = animation.FuncAnimation(
            self.fig, func=self.animate, init_func=self.plot_init,
            interval=interval, blit=True, save_count=100
        )

        if plt_show == True:
            plt.show()


    def null_func(self):
        return []


    def quit(self):
        plt.close()


if __name__ == '__main__':

    scope = Scope()

    scope.start()
