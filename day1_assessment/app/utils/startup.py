from database import get_db
import models, auth

def create_default_librarian():
    db = next(get_db())
    try:
        librarian = db.query(models.Member).filter(models.Member.name == "admin").first()
        if not librarian:
            hashed_password = auth.get_password_hash("admin123")
            librarian = models.Member(name="admin", hashed_password=hashed_password, role="librarian")
            db.add(librarian)
            db.commit()
            print("✅ Default librarian created: username='admin', password='admin123'")
    finally:
        db.close()
