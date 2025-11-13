import threading
import time

def task():
    print("Task started")
    time.sleep(3)
    print("Task finished")

t1 = threading.Thread(target=task)

t1.start()
print("Main thread waiting for t1...")
t1.join()   
print("Main thread resumes after t1 is done")
