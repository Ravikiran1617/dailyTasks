import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from sync_crud_operations.database import SessionLocal
import exceptions_db.crud_with_exc as crud_with_exc

db = SessionLocal()

# print("Creating users...")
# res1 = crud_with_exc.create_user(db, "Ravi Kiran", "ravi@example.com")
# print(res1)

# res2 = crud_with_exc.create_user(db, "Sairam", "ramsai@example.com")
# if res2['success']:
#     user = res2['user']
#     print(f"ID: {user.id}")
#     print(f"Name: {user.name}")
#     print(f"Email: {user.email}")  

# # Trying duplicate email
# res3 = crud_with_exc.create_user(db, "Another User", "ravi@example.com")
# print(res3)  # Should show error message

# print("\nAll users:")
# res = crud_with_exc.get_users(db)
# if res["success"]:
#     for user in res["data"]:
#         print(f"{user.id}: {user.name} ({user.email})")
# else:
#     print(res["error"])

print("\nUpdating user email...")
res4 = crud_with_exc.update_user_email(db, 1, "ravi.new@example.com")
print(res4)

# print("\nDeleting user...")
# res5 = crud_with_exc.delete_user(db, 2)
# print(res5)

# db.close()
