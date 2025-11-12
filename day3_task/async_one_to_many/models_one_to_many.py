from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database_one_to_many import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    
    posts = relationship("Post", back_populates="owner", cascade="all, delete", lazy="selectin")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))  

    owner = relationship("User", back_populates="posts")
