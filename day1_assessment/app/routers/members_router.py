from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, auth
from database import get_db

router = APIRouter(prefix="/members", tags=["Members"])

@router.post("/", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db),
                  current_member: models.Member = Depends(auth.require_librarian)):
    if db.query(models.Member).filter(models.Member.name == member.name).first():
        raise HTTPException(status_code=400, detail="Member already exists")

    hashed_password = auth.get_password_hash(member.password)
    db_member = models.Member(name=member.name, hashed_password=hashed_password, role=member.role)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member
