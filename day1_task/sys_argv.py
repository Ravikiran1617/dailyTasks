# sys lets your Python program talk to the system — like checking which version of Python you’re using, accessing command-line arguments, exiting the program, or modifying the module search path.
import sys

print("Python version:", sys.version)
print("Platform:", sys.platform)
print("Command-line arguments:", sys.argv)

# Add a new directory to the module search path
sys.path.append("C:/MyModules")

# Exit the program
if len(sys.argv) < 2:
    print("No arguments provided.")
    sys.exit(1)
else:
    print("Script running successfully!")

for p in sys.path:
    print(p)