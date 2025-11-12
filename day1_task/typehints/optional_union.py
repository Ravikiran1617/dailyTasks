from typing import Optional, Union

def get_user(id: int) -> Optional[str]:
    # returns string or None
    return "Ravi" if id == 1 else None

def process(value: Union[int, str]):
    print(value)
#If we want to restrict it strictly then we can use the below code 
# def process(value: Union[int, str]):
#     if not isinstance(value, (int, str)):
#         raise TypeError("Value must be int or str only.")
#     print(value)

print(get_user(1))  
print(get_user(2))   

process(100)         
process("Hello")    
process({'name':'Ravi'})  
