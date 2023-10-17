from data import stock, personnel
from datetime import datetime as dt

# Initialize is_authenticated as a global variable
user_auth_status = {}

# Initialize a list to track session actions
session_actions = []

# Decorator to check user authentication status
def authenticate_user_decorator(func):
    """
    A decorator to check if a user is authenticated before executing a function.

    Args:
        func: The function to be wrapped.

    Returns:
        wrapper: The wrapped function that checks authentication.
    """
    def wrapper(user_name, password, *args, **kwargs):
        if user_name not in user_auth_status:
            user_name = get_user_name()
            password = get_password()
            if check_user_authentication(user_name, password):
                user_auth_status[user_name] = True
                print(f" Welcome {user_name}! You are authenticated.")
            else:
                print("Invalid username or password.")
                return
        return func(user_name, password, *args, **kwargs)

    return wrapper

def get_password():
    """
    Get the user's password as input.

    Returns:
        str: The user's password.
    """
    return input("Password: ")

def get_user_name():
    """
    Get the user's name as input.

    Returns:
        str: The user's name.
    """
    return input("What is your user name? ")

def authenticate_user():
    """
    Authenticate the user based on input username and password.

    Returns:
        str: The user's name.
        bool: True if authenticated, False if not.
    """
    user_name = get_user_name()
    password = get_password()

    authenticated = check_user_authentication(user_name, password)

    if authenticated:
        user_auth_status[user_name] = True
        print(f"Welcome, {user_name}! You are authenticated.")
    else:
        print("You are logged in as a guest.")

    return user_name, authenticated

def check_user_authentication(username, password):
    """
    Check if a user's username and password match personnel data.

    Args:
        username (str): The username to check.
        password (str): The password to check.

    Returns:
        bool: True if the user is authenticated, False if not.
    """
    for user in personnel:
        if user.get('user_name') == username and user.get('password') == password:
            return True
    return False

def list_items_by_warehouse():
    """
    List items in each warehouse.
    """
    for warehouse in range(1, 4):  # Support any number of warehouses
        print(f"Items in warehouse {warehouse}:")
        for i, item in enumerate(stock, 1):
            if item['warehouse'] == warehouse:
                print(f"{i}. {item['state']} {item['category']}")

@authenticate_user_decorator
def search_and_order_item(user_name, authenticated):
    """
    Search for an item and place an order.
    
    Args:
        user_name (str): The name of the authenticated user.
        authenticated (bool): True if the user is authenticated, False if not.
    """
    while True:
        item_name = input("What is the name of the item? ").lower()
        found_items = search_items(item_name)

        if not found_items:
            print("No items found with that name.")
            show_all = input("Do you want to see all available items? (y/n) ").strip().lower()
            if show_all == 'y':
                list_items_by_warehouse()
            else:
                continue  # Ask for the name again
        else:
            print_search_results(found_items)
            if authenticated or user_name in user_auth_status:
                selected_item = get_selected_item(found_items)
                if selected_item:
                    order_item(user_name, selected_item)
            break

def search_items(item_name):
    """
    Search for items in stock based on a provided item name.

    Args:
        item_name (str): The item name to search for.

    Returns:
        list: List of found items that match the search criteria.
    """
    return [item for item in stock if item_name in (item['state'] + ' ' + item['category']).lower()]

def print_search_results(found_items):
    """
    Print the search results with item details.

    Args:
        found_items (list): List of found items.
    """
    print("Available items:")
    for i, item in enumerate(found_items, 1):
        print(f"{i}. {item['state']} {item['category']} (Warehouse {item['warehouse']}), Date of Stock: {item['date_of_stock']}")

def get_selected_item(found_items):
    """
    Get the user's selected item from the search results.

    Args:
        found_items (list): List of found items.

    Returns:
        dict: The selected item or None if canceled or invalid choice.
    """
    choice = input("Enter the number of the item you want to order (or 'cancel' to go back): ").strip().lower()
    if choice == 'cancel':
        return None
    try:
        item_choice = int(choice)
        if 1 <= item_choice <= len(found_items):
            return found_items[item_choice - 1]
        else:
            print("Invalid item number. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    return None

def order_item(user_name, selected_item):
    """
    Order an item and record the order in the item's history.

    Args:
        user_name (str): The name of the authenticated user.
        selected_item (dict): The selected item to order.
    """
    max_available_quantity = 0  # Initialize to 0
    for item in stock:
        if item['warehouse'] == selected_item['warehouse']:
            max_available_quantity += 1  # Increase the available quantity

    quantity = get_order_quantity(selected_item['state'], selected_item['category'], max_available_quantity)
    if quantity is not None:
        record_order(user_name, selected_item, quantity)
        session_actions.append(f"Ordered {quantity} of '{selected_item['state']} {selected_item['category']}' by {user_name}")

def get_order_quantity(item_state, item_category, max_available_quantity):
    """
    Get the order quantity from the user.

    Args:
        item_state (str): The state of the item.
        item_category (str): The category of the item.
        max_available_quantity (int): The maximum available quantity.

    Returns:
        int: The selected quantity or None if canceled or invalid choice.
    """
    while True:
        try:
            quantity = int(input(f"How many would you like to order for '{item_state} {item_category}' (up to {max_available_quantity}): "))
            if 0 < quantity <= max_available_quantity:
                return quantity
            else:
                print("Invalid quantity. Please enter a valid quantity within the available stock.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def record_order(user_name, selected_item, quantity):
    """
    Record an order in the item's history.

    Args:
        user_name (str): The name of the authenticated user.
        selected_item (dict): The selected item to order.
        quantity (int): The quantity to order.
    """
    order_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    order_history = selected_item.get('order_history', [])
    order_history.append({"user_name": user_name, "quantity": quantity, "order_date": order_date})
    selected_item['order_history'] = order_history
    print(f"Ordered {quantity} of '{selected_item['state']} {selected_item['category']}' by {user_name} on {order_date}.")

def browse_by_category():
    """
    Browse items by category and count the available items for each category.
    """
    category_counts = {}
    for item in stock:
        category = item['category']
        category_counts[category] = category_counts.get(category, 0) + 1

    print("Available categories:")
    i = 1
    for category, count in category_counts.items():
        print(f"{i}. {category} ({count} items)")
        i += 1

    choice = input("Type the number of the category to browse (or 'cancel' to go back): ").strip().lower()

    if choice == 'cancel':
        return

    try:
        category_choice = int(choice)
        if 1 <= category_choice <= len(category_counts):
            selected_category = list(category_counts.keys())[category_choice - 1] # -1 bcs index start from 0 
            print(f"List of {selected_category}s available:")
            for item in stock:
                if item['category'] == selected_category:
                    print(f"{item['state']} {item['category']}, Warehouse {item['warehouse']}")
            session_actions.append(f"Browsed items in the '{selected_category}' category")
        else:
            print("Invalid category number. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def get_selected_operation():
    """
    Get the selected operation from the user.

    Returns:
        str: The selected operation number.
    """
    print("What would you like to do?")
    print("1. List items by warehouse")
    print("2. Search an item and place an order")
    print("3. Browse by category")
    print("4. Quit")
    return input("Type the number of the operation: ").strip()

def handle_choice(user_name, authenticated, choice):
    """
    Handle the user's choice of operation.

    Args:
        user_name (str): The name of the authenticated user.
        authenticated (bool): True if the user is authenticated, False if not.
        choice (str): The selected operation number.
    """
    if choice == "1":
        list_items_by_warehouse()
    elif choice == "2":
        search_and_order_item(user_name, authenticated)
    elif choice == "3":
        browse_by_category()
    elif choice == "4":
        return print_finish_message(user_name, session_actions)
    else:
        print_invalid_input_message()


def print_invalid_input_message():
    """
    Print a message for invalid input.
    """
    print("Invalid input. Please choose a valid operation number.")

def print_finish_message(user_name, session_actions):
    """
    Print a message with session actions.

    Args:
        user_name (str): The name of the authenticated user.
        session_actions (list): List of session actions.
    """
    print(f"Thank you for your visit, {user_name}!")
    print("In this session, you have:")
    for i, action in enumerate(session_actions, 1):
        print(f"\t{i}. {action}.")

def main():
    """
    The main function for the program, controlling the user interaction and operations.
    """
    while True:
        user_name, authenticated = authenticate_user()
        while True:
            operation = get_selected_operation()
            if operation not in ["1", "2", "3", "4"]:
                print_invalid_input_message()
                continue

            handle_choice(user_name, authenticated, operation)
            
            another_operation = input("Do you want to perform another operation? (y/n) ").strip().lower()
            if another_operation != 'y':
                return print_finish_message(user_name, session_actions)

if __name__ == "__main__":
    main()
