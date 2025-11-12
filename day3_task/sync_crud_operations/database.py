from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# PostgreSQL connection URL
DATABASE_URL = "postgresql://postgres:root@localhost:5432/Sample_Test"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# SessionLocal will be used for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our ORM models
Base = declarative_base()

# Dependency function (useful for FastAPI or scripts)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
