import random, string, time
from sqlalchemy import select
from models_indexing import Customer
from async_many_to_many.database import AsyncSessionLocal

async def create_dummy_data():
    async with AsyncSessionLocal() as session:
        customers = []
        for _ in range(5000):
            name = ''.join(random.choices(string.ascii_lowercase, k=6))
            email = f"{name}@example.com"
            city = random.choice(["Hyderabad", "Delhi", "Bangalore", "Chennai", "Mumbai"])
            phone = ''.join(random.choices(string.digits, k=10))
            customers.append(Customer(name=name, email=email, city=city, phone=phone))

        session.add_all(customers)
        await session.commit()
        print("✅ Inserted 5000 customer records.")

async def query_without_index():
    async with AsyncSessionLocal() as session:
        start = time.time()
        result = await session.execute(select(Customer).where(Customer.city == "Hyderabad"))
        customers = result.scalars().all()
        end = time.time()
        print(f"Query (no index on 'city') took: {end - start:.5f} seconds")
        return customers

async def query_with_index():
    async with AsyncSessionLocal() as session:
        start = time.time()
        result = await session.execute(select(Customer).where(Customer.name == "ravi"))
        customers = result.scalars().all()
        end = time.time()
        print(f"Query (index on 'name') took: {end - start:.5f} seconds")
        return customers
