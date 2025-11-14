from utils.hash_utils import hash_password



fake_user_db = {
    "ravi": {
        "username": "ravi",
        "hashed_password": hash_password("password123")
    }
}


notes_db = []

 