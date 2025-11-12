from async_many_to_many.database import SessionLocal
import crud as crud

db = SessionLocal()

# # Create users
# print("Creating users...")
# crud.create_user(db, "Ravi Kiran", "ravi@example.com")
# crud.create_user(db, "Teja", "teja@example.com")

# # Read users
# print("\nAll users:")
# for user in crud.get_users(db):
#     print(f"{user.id}: {user.name} ({user.email})")  

# # Update user email
# print("\nUpdating email of user with ID=1...")
# updated = crud.update_user_email(db, 1, "ravi.kiran@newmail.com")
# print("Updated:", updated.email if updated else "User not found")

# # Delete user
# print("\nDeleting user with ID=2...")
# deleted = crud.delete_user(db, 2)
# print("Deleted successfully!" if deleted else "User not found")

# Show remaining users
print("\nFinal users:")
for user in crud.get_users(db):
    print(f"{user.id}: {user.name} ({user.email})")

db.close()
