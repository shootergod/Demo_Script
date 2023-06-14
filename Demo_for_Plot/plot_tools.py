import matplotlib
import matplotlib.pyplot as plt

import numpy as np

matplotlib.use('TkAgg')


class _base():
    def __init__(self) -> None:
        self.ax: plt.Axes = None
        self.fig = None

        self.fig, self.ax = plt.subplots()
        
        

    def show(self):
        plt.show()

    def set_title(self, info: str = ''):
        if self.ax:
            self.ax.set_title(info)

    def set_ylabel(self, info: str = ''):
        if self.ax:
            self.ax.set_ylabel(info)

        # ax.legend(title='Fruit color')


class bar(_base):
    def __init__(self, data) -> None:
        super().__init__()
        self._plot(data=data)
        # self.show()

    def _plot(self, data: np.ndarray):

        if isinstance(data, list):
            data = np.array(data)

        bin_num = 15
        v_min = np.min(data)
        v_max = np.max(data)

        x = np.linspace(v_min, v_max, bin_num + 1)
        bin_loc = (x[1:] + x[:-1]) / 2
        bin_width = (v_max - v_min) / bin_num * 0.95

        y = np.zeros(np.shape(bin_loc))
        for i in range(bin_num):
            v_l = x[i]
            v_u = x[i + 1]
            if v_u != v_max:
                tmp_height = np.size(
                    np.extract((data >= v_l) & (data < v_u), data))
            else:
                tmp_height = np.size(
                    np.extract((data >= v_l) & (data <= v_u), data))

            y[i] = tmp_height

        # ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

        self.ax.bar(bin_loc, y, width=bin_width)

        self.ax.set_ylabel('fruit supply')
        self.ax.set_title('Fruit supply by kind and color')
        # ax.legend(title='Fruit color')

        # self.fig.canvas.draw()
        # self.fig.canvas.flush_events()
        # self.fig.canvas.draw_idle()
        
        return self.fig, self.ax


# ============================================================
# test block
# ============================================================
if __name__ == '__main__':
    nums = np.random.normal(loc=10, scale=5, size=1000)



    bar(data=nums)


    nums2 = np.random.normal(loc=10, scale=5, size=1000)
    bar(data=nums2)

    




