def greet():
    print("Hello Ravi!")

def decorator_function(func):
    def wrapper():
        print("Before the function runs")
        func()
        print("After the function runs")
    return wrapper

# wrapping the greet() function
new_func = decorator_function(greet)
new_func()
