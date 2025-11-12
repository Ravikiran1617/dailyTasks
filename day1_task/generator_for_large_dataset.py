def large_number_generator(limit):
    num = 0
    while num < limit:
        yield num
        num += 1
for n in large_number_generator(10**8):
    if n % 10000000 == 0:            
        print("Processed:", n)


#here we can process large numbers dataset without crashing the system 