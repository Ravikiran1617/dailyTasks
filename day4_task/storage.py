from typing import Dict
from uuid import uuid4
from datetime import datetime
from schemas import TodoInDB, TodoBase

_db: Dict[str, dict] = {}

def create_item(data: TodoBase) -> TodoInDB:
    new_id = str(uuid4())
    now = datetime.utcnow()
    item = data.dict()
    item.update({"id": new_id, "created_at": now, "updated_at": now})
    _db[new_id] = item
    return TodoInDB(**item)

def get_item(item_id: str) -> TodoInDB | None:
    raw = _db.get(item_id)
    return TodoInDB(**raw) if raw else None

def list_items() -> list[TodoInDB]:
    return [TodoInDB(**v) for v in _db.values()]

def update_item(item_id: str, patch: dict) -> TodoInDB | None:
    existing = _db.get(item_id)
    if not existing:
        return None
    existing.update(patch)
    existing["updated_at"] = datetime.utcnow()
    _db[item_id] = existing
    return TodoInDB(**existing)

def delete_item(item_id: str) -> bool:
    return _db.pop(item_id, None) is not None
