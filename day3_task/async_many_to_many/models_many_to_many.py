from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

#Association table between Student and Library
student_library_association = Table(
    "student_library_association",
    Base.metadata,
    Column("student_id", ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
    Column("library_id", ForeignKey("libraries.id", ondelete="CASCADE"), primary_key=True)
)

#Association table between Student and School
student_school_association = Table(
    "student_school_association",
    Base.metadata,
    Column("student_id", ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
    Column("school_id", ForeignKey("schools.id", ondelete="CASCADE"), primary_key=True)
)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    grade = Column(String)

    # Relationships
    libraries = relationship(
        "Library",
        secondary=student_library_association,
        back_populates="students",
        lazy="selectin"
    )
    schools = relationship(
        "School",
        secondary=student_school_association,
        back_populates="students",
        lazy="selectin"
    )


class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)

    # Relationship back to Student
    students = relationship(
        "Student",
        secondary=student_library_association,
        back_populates="libraries",
        lazy="selectin"
    )


class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)

    # Relationship back to Student
    students = relationship(
        "Student",
        secondary=student_school_association,
        back_populates="schools",
        lazy="selectin"
    )
