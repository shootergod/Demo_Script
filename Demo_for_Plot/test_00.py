import matplotlib.pyplot as plt
import numpy as np

import matplotlib
matplotlib.use('TkAgg')

x = np.arange(1,10,0.1)
y = x**2
z = x**3+5

plt.ion() #开启interactive mode

plt.figure(1)
plt.plot(x,y)   #立即绘制图像1
# plt.pause(20)    #等待2s但是不会关闭图像1

plt.figure(2)
plt.plot(x,z)   #立即绘制图像2
# plt.pause(2)    #等待2s关闭图像1，2

plt.ioff()      #关闭interactive mode
plt.show()      #显示图像1,2并且阻塞程序