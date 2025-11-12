class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name   # getter

    @name.setter
    def name(self, value):
        if not value:
            print("Name cannot be empty!")
        else:
            self._name = value

p = Person("Ravi")
print(p.name)      # no parentheses! (calls the getter)
p.name = "Kiran"   # setting an attribute (calls the setter)  
print(p.name)

# we use setter method to set the value and getter method to get the value