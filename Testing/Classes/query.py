from loader import Loader
from classes import User, Employee, Warehouse, Item, SessionReport, WarehouseManager

personnel_loader = Loader(model="personnel")
personnel_data = personnel_loader.objects

stock_loader = Loader(model="stock")
stock = stock_loader.objects


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
    """
    Main function to run the program.
    """
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
        choice = get_selected_operation()
        if choice == "1" or (choice == "3" and not user):
            # Call the display_warehouses method
            warehouse_manager.display_warehouses()
            
            # Check if user is authenticated before saving the report and adding action
            if user.is_authenticated:
                session_report.add_action("Listed warehouses")
            
        if choice == "2":
            # Authentication check for authenticated users
            if not user.is_authenticated:
                print("Authentication required.")
                continue

            user.search_and_order_item(stock)
            
            session_report.add_action("Searched and Ordered")
            session_report.record_searched_item(user.last_searched_item)
            session_report.record_ordered_item(user.last_ordered_item_state, user.last_ordered_item_category, user.last_ordered_quantity)


        elif choice == "3":
            user.browse_by_category(stock)
            if  user.is_authenticated:
            
                session_report.add_action("Browsed Items")
                session_report.record_browsed_item(user.last_browsed_item)
            
        elif choice == "4":
            session_report.display_report()
           
            break
        
if __name__ == "__main__":
    main()