import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"
TOKEN = None
CURRENT_USER = None
CURRENT_ROLE = None


def login():
    global TOKEN, CURRENT_USER, CURRENT_ROLE
    username = input("Enter username: ")
    password = input("Enter password: ")
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            data={"username": username, "password": password}
        )
        response.raise_for_status()
        token_data = response.json()
        TOKEN = token_data["access_token"]
        print("✅ Login successful!")

        # Get user info to store role
        headers = {"Authorization": f"Bearer {TOKEN}"}
        user_response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        user_response.raise_for_status()
        user_info = user_response.json()
        CURRENT_USER = user_info
        CURRENT_ROLE = user_info["role"]
        print(f"👤 Logged in as {CURRENT_USER['name']} ({CURRENT_ROLE})")

    except requests.exceptions.HTTPError as e:
        print(f"❌ Login failed: {e.response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print("⚠️ Could not connect to the API. Is FastAPI running?")
    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")


def get_headers():
    if not TOKEN:
        print("⚠️ You must be logged in first.")
        return None
    return {"Authorization": f"Bearer {TOKEN}"}


def add_book():
    headers = get_headers()
    if not headers:
        return

    title = input("Enter book title: ")
    author = input("Enter book author: ")
    isbn = input("Enter book ISBN: ")
    book_data = {"title": title, "author": author, "isbn": isbn}

    try:
        response = requests.post(f"{BASE_URL}/books/", json=book_data, headers=headers)
        response.raise_for_status()
        print("✅ Book added successfully:", response.json())
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error adding book: {e.response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print("⚠️ Could not connect to the API. Is FastAPI running?")


def list_books():
    headers = get_headers()
    if not headers:
        return

    try:
        response = requests.get(f"{BASE_URL}/books/", headers=headers)
        response.raise_for_status()
        books = response.json()
        if books:
            print("\n📚 --- All Books ---")
            for book in books:
                status = "Available" if book['available'] else f"Borrowed by {book['borrowed_by']} (Return: {book['return_date']})"
                print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, ISBN: {book['isbn']}, Status: {status}")
            print("-----------------")
        else:
            print("No books found.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error listing books: {e.response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print("⚠️ Could not connect to the API. Is FastAPI running?")


def search_books():
    headers = get_headers()
    if not headers:
        return

    query = input("Enter search query (title or author): ")
    try:
        response = requests.get(f"{BASE_URL}/books/search?query={query}", headers=headers)
        response.raise_for_status()
        books = response.json()
        if books:
            print("\n🔍 --- Search Results ---")
            for book in books:
                status = "Available" if book['available'] else f"Borrowed by {book['borrowed_by']} (Return: {book['return_date']})"
                print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, ISBN: {book['isbn']}, Status: {status}")
            print("----------------------")
        else:
            print("No books found matching your query.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error searching books: {e.response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print("⚠️ Could not connect to the API. Is FastAPI running?")


def borrow_book():
    headers = get_headers()
    if not headers:
        return

    book_id = int(input("Enter Book ID to borrow: "))
    return_date_str = input("Enter return date (YYYY-MM-DD, e.g., 2025-12-31): ")
    try:
        datetime.strptime(return_date_str, "%Y-%m-%d")  # Validate date format
        borrow_data = {"book_id": book_id, "return_date": return_date_str}
        response = requests.post(f"{BASE_URL}/books/borrow", json=borrow_data, headers=headers)
        response.raise_for_status()
        print("✅ Book borrowed successfully:", response.json())
    except ValueError:
        print("❌ Invalid date format. Please use YYYY-MM-DD.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error borrowing book: {e.response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print("⚠️ Could not connect to the API. Is FastAPI running?")


def return_book():
    headers = get_headers()
    if not headers:
        return

    book_id = int(input("Enter Book ID to return: "))
    return_data = {"book_id": book_id}
    try:
        response = requests.post(f"{BASE_URL}/books/return", json=return_data, headers=headers)
        response.raise_for_status()
        print("✅ Book returned successfully:", response.json())
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error returning book: {e.response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print("⚠️ Could not connect to the API. Is FastAPI running?")


def list_borrowed_books():
    headers = get_headers()
    if not headers:
        return

    try:
        response = requests.get(f"{BASE_URL}/members/me/borrowed-books", headers=headers)
        response.raise_for_status()
        borrowed_books = response.json()
        if borrowed_books:
            print("\n📖 --- Your Borrowed Books ---")
            for record in borrowed_books:
                print(f"Book: {record['book_title']} (ID: {record['book_id']}), Borrowed Date: {record['borrow_date']}, Due: {record['return_date']}")
            print("---------------------------")
        else:
            print("You have no books currently borrowed.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error listing borrowed books: {e.response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print("⚠️ Could not connect to the API. Is FastAPI running?")


def add_member():
    headers = get_headers()
    if not headers:
        return

    name = input("Enter member name: ")
    password = input("Enter member password: ")
    role = input("Enter member role (librarian/member, default 'member'): ") or 'member'
    member_data = {"name": name, "password": password, "role": role}

    try:
        response = requests.post(f"{BASE_URL}/members/", json=member_data, headers=headers)
        response.raise_for_status()
        print("✅ Member added successfully:", response.json())
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error adding member: {e.response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print("⚠️ Could not connect to the API. Is FastAPI running?")


def librarian_menu():
    global TOKEN, CURRENT_USER, CURRENT_ROLE
    while True:
        print("\n--- Librarian Menu ---")
        print("1. Add Book")
        print("2. Add Member")
        print("3. List All Books")
        print("4. Search Books")
        print("5. Logout")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            add_member()
        elif choice == '3':
            list_books()
        elif choice == '4':
            search_books()
        elif choice == '5':
            TOKEN = None
            CURRENT_USER = None
            CURRENT_ROLE = None
            print("👋 Logged out.")
            break
        elif choice == '6':
            exit()
        else:
            print("Invalid choice. Please try again.")


def member_menu():
    global TOKEN, CURRENT_USER, CURRENT_ROLE
    while True:
        print("\n--- Member Menu ---")
        print("1. Borrow Book")
        print("2. Return Book")
        print("3. List All Books")
        print("4. Search Books")
        print("5. List My Borrowed Books")
        print("6. Logout")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            borrow_book()
        elif choice == '2':
            return_book()
        elif choice == '3':
            list_books()
        elif choice == '4':
            search_books()
        elif choice == '5':
            list_borrowed_books()
        elif choice == '6':
            TOKEN = None
            CURRENT_USER = None
            CURRENT_ROLE = None
            print("👋 Logged out.")
            break
        elif choice == '7':
            exit()
        else:
            print("Invalid choice. Please try again.")


def main_menu():
    global TOKEN, CURRENT_USER, CURRENT_ROLE
    while True:
        if not TOKEN:
            print("\n=== Main Menu ===")
            print("1. Login")
            print("2. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                login()
            elif choice == '2':
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            if CURRENT_ROLE == 'librarian':
                librarian_menu()
            elif CURRENT_ROLE == 'member':
                member_menu()
            else:
                print("Unknown role. Logging out.")
                TOKEN = None
                CURRENT_USER = None
                CURRENT_ROLE = None


if __name__ == "__main__":
    main_menu()
