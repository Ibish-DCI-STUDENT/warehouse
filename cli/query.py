from data import warehouse1, warehouse2

# Function to list items by warehouse
def list_items_by_warehouse():
    print("Items in warehouse 1:")
    for item in warehouse1:
        print(f"- {item}")
    print("\nItems in warehouse 2:")
    for item in warehouse2:
        print(f"- {item}")

# Function to search for an item and place an order
def search_and_order_item(item_name):
    count_warehouse1 = warehouse1.count(item_name)
    count_warehouse2 = warehouse2.count(item_name)
    
    total_available = count_warehouse1 + count_warehouse2
    
    print(f"Amount available: {total_available}")
    
    if total_available == 0:
        print("Location: Not in stock")
    elif count_warehouse1 > 0 and count_warehouse2 > 0:
        print("Location: Both warehouses")
        max_warehouse = "Warehouse 1" if count_warehouse1 > count_warehouse2 else "Warehouse 2"
        print(f"Maximum availability: {max(count_warehouse1, count_warehouse2)} in {max_warehouse}")
    elif count_warehouse1 > 0:
        print("Location: Warehouse 1")
        print(f"Maximum availability: {count_warehouse1} in Warehouse 1")
    elif count_warehouse2 > 0:
        print("Location: Warehouse 2")
        print(f"Maximum availability: {count_warehouse2} in Warehouse 2")
    
    order_choice = input("Would you like to order this item? (y/n): ").strip().lower()
    
    if order_choice == "y":
        desired_amount = int(input("How many would you like? "))
        
        if desired_amount <= total_available:
            print(f"{desired_amount} {item_name} have been ordered.")
        else:
            max_available = min(desired_amount, total_available)
            print("**************************************************")
            print(f"There are not this many available. The maximum amount that can be ordered is {max_available}")
            print("**************************************************")
            
            max_order_choice = input("Would you like to order the maximum available? (y/n): ").strip().lower()
            if max_order_choice == "y":
                print(f"{max_available} {item_name} have been ordered.")
    else:
        print("Order not placed.")

# Get the user name
user_name = input("What is your user name? ")
print(f"Hello, {user_name}!")

# Show the menu and ask to pick a choice
while True:
    print("What would you like to do?")
    print("1. List items by warehouse")
    print("2. Search an item and place an order")
    print("3. Quit")
    
    choice = input("Type the number of the operation: ").strip()

    if choice == "1":
        list_items_by_warehouse()
    elif choice == "2":
        item_name = input("What is the name of the item? ")
        search_and_order_item(item_name)
    elif choice == "3":
        print(f"Thank you for your visit, {user_name}!")
        break
    else:
        print("**************************************************")
        print("Invalid operation entered. Please choose a valid operation (1, 2, or 3).")
        print("**************************************************")
