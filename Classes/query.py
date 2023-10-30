from loader import Loader
from classes import User, Employee, Warehouse, Item, SessionReport, WarehouseManager

def display_warehouses(stock):
    for warehouse in stock:
        print(f"Warehouse {warehouse.id} - Stock Count: {warehouse.occupancy()}")

def get_authenticated_user(personnel_data):
    user_name = input("Enter your name: ")
    user_password = input("Enter your password: ")

    for employee in personnel_data:
        if employee.is_named(user_name):
            user = employee
            break
    else:
        user = None

    if user and user_password:
        user.authenticate(user_password)
        if user.is_authenticated:
            print(f"Welcome, {user_name}! You are authenticated.")
        else:
            print(f"Authentication failed for user {user_name}.")
    elif user_password:
        print("Password required for authentication.")
    return user

def main():
    personnel_loader = Loader(model="personnel")
    stock_loader = Loader(model="stock")

    personnel_data = personnel_loader.objects
    stock = stock_loader.objects

    guest_user = User("Guest")

    while True:
        print("1. Enter as Guest")
        print("2. Enter as Authenticated User")
        choice = input("Enter your choice: ")

        if choice == "1":
            user = guest_user
            break
        elif choice == "2":
            user = get_authenticated_user(personnel_data)
            if not user:
                print("User not found. Please ask one of our staff members for assistance.")
                continue
            else:
                break
        else:
            print("Invalid choice. Please select option 1 or 2.")

    session_report = SessionReport(user)
    # Create an instance of WarehouseManager
    warehouse_manager = WarehouseManager(stock)

    while True:
        choice = user.get_selected_operation()
        if choice == "1" or (choice == "3" and not user):
            # Call the display_warehouses method
            warehouse_manager.display_warehouses()
            session_report.add_action("Listed warehouses")
            
        if choice == "2":
            # Authentication check for authenticated users
            if user != User("Guest") and not user.is_authenticated:
                print("Authentication required.")
                continue

            user.search_and_order_item(stock)
            
            session_report.add_action("Searched and Ordered")
            session_report.record_searched_item(user.last_searched_item)
            session_report.record_ordered_item(user.last_ordered_item_state, user.last_ordered_item_category, user.last_ordered_quantity)


        elif choice == "3":
            user.browse_by_category(stock)
            
            session_report.add_action("Browsed Items")
            session_report.record_browsed_item(user.last_browsed_item)
            
        elif choice == "4":
            session_report.display_report()
            break
        
if __name__ == "__main__":
    main()