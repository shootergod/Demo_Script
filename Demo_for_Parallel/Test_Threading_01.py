import threading

# inherit from bass
class MyThread(threading.Thread):
    def __init__(self, thread_name):
        # super(MyThread, self).__init__(name=thread_name)
        super().__init__(name=thread_name)

    # override method
    def run(self):
        print("Thread %s is running ..." % self.name)

# ============================================================
# test block
# ============================================================
if __name__ == '__main__':
    for i in range(10):
        thread_name = "TestThread_" + str(i)
        tmp_thread_obj = MyThread(thread_name)
        tmp_thread_obj.start()