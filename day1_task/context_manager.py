######### Context Managers :objects that manage resources like files or network connections
# Imagine you open a file — you should close it when done.
# If an error happens, the file might not close properly.

# To make sure it always closes, we use a context manager with a with statement.
#-----------------------------------------------------
# with open("test.txt", "w") as f:
#     f.write("Hello world")
#-------------------------------------------
# After this block ends, Python automatically closes the file, even if something goes wrong.

class MyManager:
    def __enter__(self):
        print("Start: Opening something")
        try:
            b = 2 / 0
        except ZeroDivisionError as e:
            print("Error inside __enter__:", e)
        return "Resource in use"

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("End: Closing or cleaning up")

with MyManager() as x:
    print(x)


# exc_type	The type (class) of the exception that occurred inside the with block	<class 'ZeroDivisionError'>
# exc_val	The actual exception instance (the error message or object)	ZeroDivisionError('division by zero')
# exc_tb	The traceback object — contains information about where the exception occurred (line number, etc.)	<traceback object at 0x...>

# If no exception occurs inside the with block, all three parameters are None.