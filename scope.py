import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Scope():

    def __init__(self):

        self.fig, self.ax = plt.subplots(2, 1)

        self.lines = []

        self.xlen = 1000

        self.x = np.arange(0, self.xlen, 1)
        self.y = []

        self.callback = None

        self.c = ['blue', 'red', 'green']

        for i in range(len(self.ax)):
            line = plt.Line2D(self.x , np.zeros(len(self.x)), color=self.c[i])
            self.lines.append(line)

        for i in range(len(self.ax)):
            self.ax[i].set_xlim([0, self.xlen])
            self.ax[i].set_ylim([-40000, 40000])
            self.ax[i].grid()
            

    def plot_init(self):
        for i in range(len(self.lines)):
            self.y.append(np.zeros(len(self.x)))
            self.lines[i].set_ydata(self.y[i])
            self.ax[i].add_line(self.lines[i])

        return self.lines

    def animate(self, frame):

        data = self.callback()

        for i in range(len(data)):

            self.y[0][0] = data[i][0]
            self.y[1][0] = data[i][1]

            self.y[0] = np.roll(self.y[0], -1)
            self.y[1] = np.roll(self.y[1], -1)

        for i in range(len(self.lines)):
            self.lines[i].set_ydata(self.y[i])

        return self.lines

    def start(self):

        self.ani = animation.FuncAnimation(
            self.fig, func=self.animate, init_func=self.plot_init,
            interval=20, blit=True, save_count=100
        )

        plt.show()



if __name__ == '__main__':

    scope = Scope()

    scope.start()
