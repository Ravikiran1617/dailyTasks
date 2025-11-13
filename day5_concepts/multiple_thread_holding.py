import threading
import time

def task(name):
    print(f"{name} started")
    time.sleep(2)
    print(f"{name} finished")

threads = []

# Create multiple threads
for i in range(3):
    t = threading.Thread(target=task, args=(f"Thread-{i}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("All threads completed")


# | You want to...                | Use...              |
# | ----------------------------- | ------------------- |
# | Wait until one thread is done | `.join()`           |
# | Wait for all threads          | Loop over `.join()` |
# | Pause a thread                | `time.sleep()`      |
