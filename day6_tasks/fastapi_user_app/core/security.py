import bcrypt

def hash_password(password: str) -> str:
    """Generate a bcrypt hash for a password"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))



# Hashing = Pwd+ random String(S1) 
# bcrypt=== S1  +  plain_Pwd 
# user1 = 123456 + S1  === S1 
user2 = 123456 + s2 