import threading
import time


# global var
g_num = 0
# init a locker
mutex = threading.Lock()

def test1(num):
    global g_num
    for i in range(num):
        mutex.acquire()
        g_num += 1
        mutex.release()
    print("-----in testl g_num=%d----" % g_num)

def test2(num):
    global g_num
    for i in range(num):
        mutex.acquire()
        g_num += 1
        mutex.release()
    print("-----in test2 g_num=%d=----" % g_num)

def main():
    t1 = threading.Thread(target=test1, args=(1000000,))
    t2 = threading.Thread(target=test2, args=(1000000,))
    t1.start()
    t2.start()
    # wait for sub-threads finish their works
    time.sleep(2)
    print("-----in main Thread g_num = %d---" % g_num)

# ============================================================
# test block
# ============================================================
if __name__ == '__main__':
    main()