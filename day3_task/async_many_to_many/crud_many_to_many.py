from models_many_to_many import Student, Library, School
from database import AsyncSessionLocal

async def create_initial_data():
    async with AsyncSessionLocal() as session:
        # Students
        student1 = Student(name="Ravi Kiran", grade="A")
        student2 = Student(name="Sai Ashrith", grade="B")

        # Libraries
        library1 = Library(name="Central Library", location="Hyderabad")
        library2 = Library(name="Knowledge Hub", location="Bangalore")

        # Schools
        school1 = School(name="Little Flower High School", address="Madhapur")
        school2 = School(name="Future Minds Academy", address="Kukatpally")

        # Establish relationships
        student1.libraries.extend([library1, library2])
        student2.libraries.append(library1)

        student1.schools.append(school1)
        student2.schools.append(school2)

        session.add_all([student1, student2, library1, library2, school1, school2])
        await session.commit()

        print("Initial data created with relationships.")


async def fetch_all_data():
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        result = await session.execute(select(Student))
        students = result.scalars().unique().all()

        for s in students:
            print(f"\n Student: {s.name} (Grade {s.grade})")

            print(" Libraries:")
            for lib in s.libraries:
                print(f"     - {lib.name} ({lib.location})")

            print("  Schools:")
            for sch in s.schools:
                print(f"     - {sch.name} ({sch.address})")
