# ============================================================
# import
# ============================================================
import os
import threading

import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')




# ============================================================
# test block
# ============================================================
cwd = os.path.dirname(os.path.abspath(__file__))
fn = 'temp.png'
fp = os.path.join(cwd, fn)


# ============================================================
# data
# ============================================================
def plot1():
    

    fig1, ax1 = plt.subplots()

    freqs = np.arange(2, 20, 3)
    t = np.arange(0.0, 1.0, 0.001)
    s = np.sin(2 * np.pi * freqs[0] * t)
    line1, = ax1.plot(t, s, lw=2)

    # plt.savefig(fp, dpi=500, bbox_inches='tight')
    plt.show()

    print('plot 1 ok')


def plot2():
    

    fig1, ax1 = plt.subplots()

    freqs = np.arange(2, 20, 3)
    t = np.arange(0.0, 1.0, 0.001)
    s = np.sin(2 * np.pi * freqs[2] * t)
    line1, = ax1.plot(t, s, lw=2)

    # plt.savefig(fp, dpi=500, bbox_inches='tight')
    plt.show()

    print('plot 2 ok')


# ============================================================
# test block
# ============================================================
if __name__ == '__main__':
    t1 = threading.Thread(target=plot1)
    t2 = threading.Thread(target=plot2)


    t1.start()
    t2.start()

