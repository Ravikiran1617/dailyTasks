import cProfile
import time

def slow_function():
    total = 0
    for i in range(1000000):
        total += i
    time.sleep(1)
    return total

cProfile.run('slow_function()')
