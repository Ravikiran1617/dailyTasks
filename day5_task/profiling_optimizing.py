import cProfile
import time

def slow_function():
    total = 0
    for i in range(1000000):
        total += i
    time.sleep(1)
    print(total) 
    return total 

res = cProfile.run('slow_function()')
print(res) 
