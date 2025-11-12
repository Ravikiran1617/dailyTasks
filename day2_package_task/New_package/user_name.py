from Old_package import get_name

def greet(name: str) -> str:
    return f"Hello, {name}"
name = get_name.get_user_name()
res = greet(name)
print(res) 