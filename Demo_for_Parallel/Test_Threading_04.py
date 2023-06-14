import threading
import time

# a global number
number = 0


def add():
    # refer to it
    global number

    for _ in range(1000000):
        number += 1

    print('Sub-Threading %s Finished, Rst Number = %d \n' %
          (threading.current_thread().getName(), number))


# ============================================================
# test block
# ============================================================
if __name__ == '__main__':
    print('Main-Threading %s Start, Rst Number = %d \n' %
          (threading.current_thread().getName(), number))
    for i in range(2):
        t = threading.Thread(target=add)
        t.start()

    time.sleep(3)

    print('Main-Threading %s Finished, Rst Number = %d \n' %
          (threading.current_thread().getName(), number))

