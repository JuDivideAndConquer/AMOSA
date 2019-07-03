import matplotlib.pyplot as plt
from matplotlib import axes
from itertools import count
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d


def real_time_plot(data):
    x = []
    y = []
    z = []
    index = count()

    def animate(i):
        ind = int(next(index))
        if(ind == len(data)):
            plt.close()
            return
        x = data[ind][0]
        y = data[ind][1]
        z = data[ind][2]
        plt.cla()
        plt.tight_layout()
        plt.title(str(ind))
        plt.suptitle(ind)
        ax = plt.axes(projection='3d')
        ax.scatter3D(x, y, z)
        ax.set_xlabel(str(ind))

    ani = FuncAnimation(plt.gcf(), animate, 10)
    plt.show()
