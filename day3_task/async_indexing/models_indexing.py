from sqlalchemy import Column, Integer, String, Index
from async_many_to_many.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)  
    email = Column(String(100), unique=True, index=True)
    city = Column(String(50))              
    phone = Column(String(20))

# Composite index (multiple columns)
Index("ix_customers_name_city", Customer.name, Customer.city)
