from schemas import TodoCreate, TodoUpdate
import storage

def create_todo(payload: TodoCreate):
    return storage.create_item(payload)

def get_todo_by_id(todo_id: str):
    return storage.get_item(todo_id)

def list_todos():
    return storage.list_items()

def update_todo(todo_id: str, payload: TodoUpdate):
    patch = {k: v for k, v in payload.dict().items() if v is not None}
    return storage.update_item(todo_id, patch)

def remove_todo(todo_id: str):
    return storage.delete_item(todo_id)
