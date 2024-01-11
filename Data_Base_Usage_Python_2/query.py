#query.py
from classes import SessionReport, User,Warehouse,Employee 
from loader import Loader
import os
import json
from datetime import datetime

personnel_data = Loader(model="personnel")
stock = Loader(model="stock")

def guest_login():
    guest_name = input("Enter your name: ")
    guest_user = User(guest_name)
    guest_user.greet()
    return guest_user

def get_authenticated_user(personnel_data):

    user_name = input("Enter your name: ")
    user_password = input("Enter your password: ")

    for employee in personnel_data:
        if employee.is_named(user_name) and user_password == employee.password:
            employee.is_authenticated = True
            print(f"\nWelcome, {user_name}! You are authenticated.")

            return employee  # Return the authenticated Employee object

    print(f"Authentication failed for user {user_name}.")
    return None  # Return None for failed authentication
def get_selected_operation() -> str:
    while True:
        print("1. Display Warehouses")
        print("2. Search and Order Item")
        print("3. Browse by Category")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice in ["1", "2", "3", "4"]:
            return choice
        else:
            print("Invalid choice. Please select a valid option.")
def main():
    user = None
    while True:
        print("1. Enter as Guest")
        print("2. Enter as Authenticated User")

        choice = input("Enter your choice: ")
        if choice == "1":
            user = guest_login()

            user.greet()
            break

        elif choice == "2":
            user = get_authenticated_user(personnel_data)

            user.employee_greet()
            if not user:
                print(
                    "User not found."
                    "Please ask one of our staff members for assistance."
                )
                continue
            else:
                break
        else:
            print("Invalid choice. Please select option 1 or 2.")

    session_report = SessionReport(user)
    while True:
        choice = get_selected_operation()

        if choice == "1":
            user.display_warehouses(stock)

        if choice == "2":
            # Authentication check for authenticated users
            if not user.is_authenticated:
                print("Authentication required for this action.")
                continue

            user.search_and_order_item(stock)

            session_report.add_action("Searched and Ordered")
            session_report.record_searched_item(user.last_searched_item)
            session_report.record_ordered_item(
                user.last_ordered_item_state,
                user.last_ordered_item_category,
                user.last_ordered_quantity,)

        elif choice == "3":
            user.browse_by_category(stock)
            if user:
                session_report.add_action("Browsed Items")
                session_report.record_browsed_item(user.last_browsed_item)

        elif choice == "4":
            session_report.display_report()
            session_report.save_to_log()  # Save the session report to a log file
            break

if __name__ == "__main__":
    main()