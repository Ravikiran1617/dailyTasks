from fastapi import FastAPI, HTTPException, status
from typing import List
import crud
from schemas import TodoCreate, TodoUpdate, TodoInDB

app = FastAPI(title="Simple ToDo API", version="1.0.0")

@app.post("/todos", response_model=TodoInDB, status_code=status.HTTP_201_CREATED)
def create_todo(item: TodoCreate):
    created = crud.create_todo(item)
    return created

@app.get("/todos", response_model=List[TodoInDB])
def read_todos():
    return crud.list_todos()

@app.get("/todos/{todo_id}", response_model=TodoInDB)
def read_todo(todo_id: str):
    todo = crud.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoInDB)
def update_todo(todo_id: str, item: TodoUpdate):
    updated = crud.update_todo(todo_id, item)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return updated

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: str):
    deleted = crud.remove_todo(todo_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return
