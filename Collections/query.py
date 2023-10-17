from datetime import datetime as dt 
from sample.data import stock 

# Function to list all items by warehouse
def list_items_by_warehouse():
    for warehouse in range(1, 3):
        print(f"Items in warehouse {warehouse}:")
        for item in stock:
            if item['warehouse'] == warehouse:
                print(f"- {item['state']} {item['category']}")
                print(f"Thank you for your visit, {user}!")
                
    
    # Calculate the total items in each warehouse
    total_items_warehouse1 = sum(1 for item in stock if item['warehouse'] == 1)
    total_items_warehouse2 = sum(1 for item in stock if item['warehouse'] == 2)

    # Print the total items in each warehouse
    print(f"Total items in warehouse 1: {total_items_warehouse1}")
    print(f"Total items in warehouse 2: {total_items_warehouse2}")
    
# Function to search and order an item
def search_and_order_item(item_name):
    
    item_name = item_name.lower()

    found_items = []
    for item in stock:
        item_full_name = (item['state'] + ' ' + item['category']).lower()
        if item_name in item_full_name:
            found_items.append(item)

    if found_items:
        print("Amount available:")
        for item in found_items:
            # Convert the date_of_stock string to a datetime object
            date_of_stock = dt.strptime(item['date_of_stock'], '%Y-%m-%d %H:%M:%S')

            days_in_stock = (dt.now() - date_of_stock).days
            print(f"- Warehouse {item['warehouse']} (in stock for {days_in_stock} days)")

        # Check if the item is in more than one warehouse
        warehouse_counts = {}
        for item in found_items:
            warehouse_counts[item['warehouse']] = warehouse_counts.get(item['warehouse'], 0) + 1

        max_count = max(warehouse_counts.values())
        max_warehouses = [warehouse for warehouse, count in warehouse_counts.items() if count == max_count]

        if len(max_warehouses) == 1:
            max_warehouse = max_warehouses[0]
            print(f"Maximum availability: {max_count} in Warehouse {max_warehouse}")
        else:
            print(f"Maximum availability: {max_count} in Warehouses {', '.join(map(str, max_warehouses))}")

        # Ask if the user wants to place an order
        order_choice = input("Would you like to order this item?(y/n) ").strip().lower()
        if order_choice == "y":
            order_quantity = int(input("How many would you like? "))
            if order_quantity <= max_count:
                print(f"{order_quantity} {item_name.capitalize()} have been ordered.")
            else:
                print("**************************************************")
                print("There are not this many available. The maximum amount that can be ordered is", max_count)
                order_choice = input("Would you like to order the maximum available?(y/n) ").strip().lower()
                if order_choice == "y":
                    print(f"{max_count} {item_name.capitalize()} have been ordered.")
    else:
        print(f"Amaunt availability: 0 ")
        print("Location: Not in stock")


# Function to browse items by category
def browse_by_category():
    categories = set(item['category'] for item in stock)

    print("Available categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")

    category_choice = input("Type the number of the category to browse (or 'cancel' to go back): ")
    if category_choice == 'cancel':
        return

    try:
        category_choice = int(category_choice)
        if 1 <= category_choice <= len(categories):
            selected_category = list(categories)[category_choice - 1]
            print(f"List of {selected_category}s available:")
            for item in stock:
                if item['category'] == selected_category:
                    print(f"{item['state']} {item['category']}, Warehouse {item['warehouse']}")
        else:
            print("Invalid category number. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a number.")
# Main function
def main():
    user_name = input("What is your user name? ")

    print(f"Hello, {user_name}!")

    while True:
        print("What would you like to do?")
        print("1. List items by warehouse")
        print("2. Search an item and place an order")
        print("3. Browse by category")
        print("4. Quit")

        choice = input("Type the number of the operation: ").strip()

        if choice == "1":
            list_items_by_warehouse()
        elif choice == "2":
            item_name = input("What is the name of the item? ")
            search_and_order_item(item_name)
        elif choice == "3":
            browse_by_category()
        elif choice == "4":
            print(f"Thank you for your visit, {user_name}!")
            break
        else:
            print("Invalid input. Please choose a valid operation number.")

if __name__ == "__main__":
    main()
