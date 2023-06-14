import threading


def show(num):
    print("Thread %s is running ..." % num)


# ============================================================
# test block
# ============================================================
if __name__ == '__main__':
    for i in range(10):
        t = threading.Thread(target=show, args=(i, ))
        t.start()