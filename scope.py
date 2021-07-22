import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Scope():

    def __init__(self, num_of_channels=2, data_len=1000, fps=50):

        self.enable = False

        self.num_of_channels=num_of_channels
        self.data_len = data_len
        self.fps = fps

        self.fig, self.ax = plt.subplots(self.num_of_channels, 1)

        self.lines = []

        self.x = np.arange(0, self.data_len, 1)
        self.y = []

        self.callback = None

        self.c = ['blue', 'red', 'green']

        for i in range(len(self.ax)):
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
            self.ax[i].add_line(self.lines[i])

        return self.lines

    def animate(self, frame):

        data = self.callback()

        for i in range(len(data)):

            for j in range(self.num_of_channels):
                self.y[j][0] = data[i][j]
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



if __name__ == '__main__':

    scope = Scope()

    scope.start()
