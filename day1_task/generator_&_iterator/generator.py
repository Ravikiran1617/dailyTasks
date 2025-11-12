# A generator automatically creates an iterator for you.

# You use the yield keyword instead of return.

# It remembers where it left off, so next time you call it, it continues from there.

def simple_generator():
    for i in range(10):
        yield i

gen = simple_generator()

for i in gen:
    print(i) 
