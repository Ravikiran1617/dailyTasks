from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

import models, schemas, auth
from database import get_db

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db),
                current_member: models.Member = Depends(auth.require_librarian)):
    if db.query(models.Book).filter(models.Book.isbn == book.isbn).first():
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")

    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/", response_model=List[schemas.Book])
def list_books(skip: int = 0, limit: int = 100,
               db: Session = Depends(get_db),
               current_member: models.Member = Depends(auth.get_current_member)):
    return db.query(models.Book).offset(skip).limit(limit).all()

@router.get("/search", response_model=List[schemas.Book])
def search_books(query: str, db: Session = Depends(get_db),
                 current_member: models.Member = Depends(auth.get_current_member)):
    return db.query(models.Book).filter(
        (models.Book.title.contains(query)) | (models.Book.author.contains(query))
    ).all()

@router.post("/borrow")
def borrow_book(borrow_request: schemas.BorrowRequest, db: Session = Depends(get_db),
                current_member: models.Member = Depends(auth.get_current_member)):
    book = db.query(models.Book).filter(models.Book.id == borrow_request.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.available:
        raise HTTPException(status_code=400, detail="Book is not available")

    book.available = False
    book.borrowed_by = current_member.name
    book.return_date = borrow_request.return_date

    borrow_record = models.BorrowRecord(
        book_id=book.id,
        member_id=current_member.id,
        return_date=borrow_request.return_date
    )

    db.add(borrow_record)
    db.commit()
    db.refresh(book)
    return {"message": "Book borrowed successfully", "book": book}

@router.post("/return")
def return_book(return_request: schemas.ReturnRequest, db: Session = Depends(get_db),
                current_member: models.Member = Depends(auth.get_current_member)):
    book = db.query(models.Book).filter(models.Book.id == return_request.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.borrowed_by != current_member.name:
        raise HTTPException(status_code=400, detail="You have not borrowed this book")

    borrow_record = db.query(models.BorrowRecord).filter(
        models.BorrowRecord.book_id == book.id,
        models.BorrowRecord.member_id == current_member.id,
        models.BorrowRecord.returned == False
    ).first()

    if borrow_record:
        borrow_record.returned = True
        borrow_record.actual_return_date = datetime.utcnow()

    book.available = True
    book.borrowed_by = None
    book.return_date = None

    db.commit()
    db.refresh(book)
    return {"message": "Book returned successfully", "book": book}

@router.get("/my-borrowed-books", response_model=List[schemas.BorrowRecordResponse])
def get_my_borrowed_books(db: Session = Depends(get_db),
                          current_member: models.Member = Depends(auth.get_current_member)):
    records = db.query(models.BorrowRecord).filter(
        models.BorrowRecord.member_id == current_member.id,
        models.BorrowRecord.returned == False
    ).all()

    return [{
        "id": r.id,
        "book_id": r.book_id,
        "book_title": r.book.title,
        "borrow_date": r.borrow_date,
        "return_date": r.return_date,
        "returned": r.returned
    } for r in records]
