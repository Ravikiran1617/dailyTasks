import threading

# Shared variable (global)
counter = 0

# Function that changes the shared variable
def increase():
    global counter
    for _ in range(10000000):
        counter += 1

# Create two threads that both modify the same variable
t1 = threading.Thread(target=increase)
t2 = threading.Thread(target=increase)

# Start both threads
t1.start()
t2.start()

# Wait for both to finish
t1.join()
t2.join()

print("Final counter value:", counter)
