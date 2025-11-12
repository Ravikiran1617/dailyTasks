from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="member")  # "librarian" or "member"
    created_at = Column(DateTime, default=datetime.utcnow)

    borrowed_books = relationship("BorrowRecord", back_populates="member")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, index=True, nullable=False)
    available = Column(Boolean, default=True)
    borrowed_by = Column(String, nullable=True)
    return_date = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    borrow_records = relationship("BorrowRecord", back_populates="book")

class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(String, nullable=False)
    returned = Column(Boolean, default=False)
    actual_return_date = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="borrow_records")
    member = relationship("Member", back_populates="borrowed_books")