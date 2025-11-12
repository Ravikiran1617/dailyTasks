from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MemberBase(BaseModel):
    name: str
    role: str = "member"

class MemberCreate(MemberBase):
    password: str

class Member(MemberBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    available: bool
    borrowed_by: Optional[str] = None
    return_date: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class BorrowRequest(BaseModel):
    book_id: int
    return_date: str

class ReturnRequest(BaseModel):
    book_id: int

class BorrowRecordResponse(BaseModel):
    id: int
    book_id: int
    book_title: str
    borrow_date: datetime
    return_date: str
    returned: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None