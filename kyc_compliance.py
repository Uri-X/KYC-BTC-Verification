import json
import os
from datetime import datetime

USER_DATA_FILE = "users.json"
TREND_DATA_FILE = "trends.json"

def load_data(filename):
    """Load JSON data from a file."""
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return {}

def save_data(filename, data):
    """Save JSON data to a file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def update_trend_data(trend_type):
    """Update trend data for registrations, document reviews, and approvals."""
    trend_data = load_data(TREND_DATA_FILE)
    current_date = datetime.now().strftime("%Y-%m-%d")

    if trend_type not in trend_data:
        trend_data[trend_type] = {}

    if current_date in trend_data[trend_type]:
        trend_data[trend_type][current_date] += 1
    else:
        trend_data[trend_type][current_date] = 1

    save_data(TREND_DATA_FILE, trend_data)

def register_user():
    """Register a new user and check eligibility."""
    email = input("Enter the user's email: ").strip()
    name = input("Enter the user's name: ").strip()
    age = int(input("Enter the user's age: ").strip())

    if age < 18:
        print(f"User '{name}' is not eligible to register (underage).")
        return

    users = load_data(USER_DATA_FILE)
    if email in users:
        print(f"User with email '{email}' already exists.")
        return

    users[email] = {
        "name": name,
        "age": age,
        "approved": False,
        "documents": {
            "photo": False,
            "id": False,
            "proof_of_residence": False
        }
    }

    save_data(USER_DATA_FILE, users)
    update_trend_data("registrations")
    print(f"User '{name}' registered successfully.")

def submit_document(email):
    """Submit and review documents for a user."""
    users = load_data(USER_DATA_FILE)

    if email not in users:
        print(f"No user found with email '{email}'.")
        return

    user = users[email]
    documents = user["documents"]

    # Review and validate documents
    for doc_type in documents:
        is_valid = input(f"Is the {doc_type.replace('_', ' ')} valid? (y/n): ").strip().lower()
        documents[doc_type] = is_valid == 'y'

    # Update approval status
    user["approved"] = all(documents.values())
    users[email] = user
    save_data(USER_DATA_FILE, users)

    update_trend_data("document_reviews")
    if user["approved"]:
        update_trend_data("approvals")
        print(f"User '{email}' approved.")
    else:
        print(f"User '{email}' not approved.")

def check_pending_users():
    """Display the number of users pending approval and allow viewing details."""
    users = load_data(USER_DATA_FILE)
    pending_users = {email: user for email, user in users.items() if not user["approved"]}

    pending_count = len(pending_users)
    print(f"Number of pending users: {pending_count}")

    if pending_count == 0:
        return

    # Option to view details
    view_details = input("Would you like to view details of pending users? (y/n): ").strip().lower()
    if view_details == 'y':
        print("\nPending Users Details:")
        for email, user in pending_users.items():
            print(f"Email: {email}, Name: {user['name']}")

def review_trend_data():
    """Review trend data for registrations, document reviews, approvals, and pending users."""
    trend_data = load_data(TREND_DATA_FILE)
    if not trend_data:
        print("No trend data available.")
        return

    print("Trend Data:")
    for trend_type, data in trend_data.items():
        print(f"\n{trend_type.capitalize()}:")
        for date, count in sorted(data.items()):
            print(f"Date: {date}, Count: {count}")

def main():
    while True:
        print("\nKYC Compliance Tool")
        print("1. Register a new user")
        print("2. Submit and review documents")
        print("3. Review trend data")
        print("4. Check pending users")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            email = input("Enter the user's email: ").strip()
            submit_document(email)
        elif choice == "3":
            review_trend_data()
        elif choice == "4":
            check_pending_users()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
