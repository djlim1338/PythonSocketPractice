#
# MultiThread.py
# djlim
#

import threading
import time


def thread_hello(name):
    t = threading.current_thread()
    print(f"hello {name}!!  {t.name}")
    time.sleep(10)
    print("thread t1 exits...")


def thread_operation():
    t = threading.current_thread()
    print(f"thread name : {t.name}")
    time.sleep(20)
    print(f"{t.name} exits...")


t1 = threading.Thread(target=thread_hello, args=('lim',))
t1.start()
# t1.join()  # t1이 종료될 때 까지 메인 중단

t2 = threading.Thread(target=thread_operation, name='Second thread', daemon=True)
t2.start()

print("main thread exits...")
