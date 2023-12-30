from datetime import datetime
from collections import Counter
from typing import List, Tuple, Dict

class Item:
    def __init__(self, state, category, warehouse, date_of_stock):
        self.state = state
        self.category = category
        self.warehouse = warehouse
        self.date_of_stock = date_of_stock

    def __str__(self):
        return f"{self.state} {self.category}"


class Warehouse:
    def __init__(self, warehouse_id=None):
        self.id = warehouse_id
        self.stock = []

    def occupancy(self) -> int:
        return len(self.stock)

    def add_item(self, item: Item) -> None:
        self.stock.append(item)

    # string represantation
    def __str__(self) -> str:
        return f"Warehouse {self.id}"

    def search(self, search_term: str) -> List[Item]:
        return [
            item for item in self.stock if search_term.lower() in item.category.lower()
        ]


class WarehouseManager:
    def __init__(self, stock: List[Warehouse]):
        self.stock = stock

    def display_warehouses(self) -> str:
        total_item_count = 0

        for warehouse in self.stock:
            stock_count = warehouse.occupancy()
            total_item_count += stock_count

            print(f"Warehouse {warehouse.id} - Stock Count: {stock_count}")

        print(f"Listed {total_item_count} items.")
        return f"Listed {total_item_count} items."

    def __str__(self) -> str:
        return f"{self.state} {self.category}"


class User:
    def __init__(self, user_name: str = "Anonymous", password=None):
        self._name = user_name
        self.is_authenticated = False
        self.password = password

    def authenticate(self, provided_password: str) -> None:
        if provided_password == self.password:
            self.is_authenticated = True

    def is_named(self, name: str) -> bool:
        return name == self._name

    def greet(self):
        if self._name:
            print(f"Hello, {self._name}!\nWelcome to our Warehouse.")
        else:
            print("Hello, Anonymous!\nWelcome to our Warehouse.")
        print(
            "If you don't find what you are looking for, please ask one of our staff members to assist you."
        )

    def employee_greet(self):
        print(
            f"\nIf you experience a problem with the system,\n"
            f"Please contact technical support.\n"
        )

    def bye(self, actions: List[str] = None) -> None:
        if actions:
            print(f"Thank you for your visit, {self._name}!")
            print("Session Actions:")
            for action in actions:
                print(action)
        else:
            print(f"Thank you for your visit, {self._name}!")

    def browse_by_category(self, stock: List[Warehouse]) -> None:
        categories = Counter()
        for warehouse in stock:
            for item in warehouse.stock:
                category = item.category.lower()
                categories[category] += 1

        print("Available categories:")
        for i, (category, count) in enumerate(categories.items(), 1):
            print(f"{i}. {category} ({count} items)")

        choice = (
            input(
                "Type the number of the category to browse (or 'cancel' to go back): "
            )
            .strip()
            .lower()
        )
        if choice == "cancel":
            return

        try:
            category_choice = int(choice)
            if 1 <= category_choice <= len(categories):
                selected_category = list(categories.keys())[category_choice - 1]

                self.last_browsed_item = selected_category  # Set the last browsed item
                self.last_browsed_quantity = categories[
                    selected_category
                ]  # Set the last browsed quantity

                print(f"List of {selected_category}s available:")

                found_items = []
                for warehouse in stock:
                    for item in warehouse.stock:
                        if item.category.lower() == selected_category:
                            found_items.append(item)

                for item in found_items:
                    print(
                        f"{item.state} ({item.category}) - Stocked on: {item.date_of_stock}"
                    )
            else:
                print("Invalid category number. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


class Employee(User):
    def __init__(self, user_name=None, password=None, **kwargs):
        super().__init__(user_name, password)
        self.password = password
        if "head_of" in kwargs:
            self.head_of = [Employee(**employee) for employee in kwargs["head_of"]]
        else:
            self.head_of = []

        # Initialize attributes for the last searched, browsed, and ordered items
        self.last_searched_item = None
        self.last_browsed_item = None
        self.last_browsed_quantity = None
        self.last_ordered_item = None  # Updated to None initially
        self.last_ordered_quantity = None
        self.last_ordered_item_state = None  # New attributes
        self.last_ordered_item_category = None

    def search_and_order_item(self, stock: List[Warehouse]) -> None:
        # Authentication check
        if not self.is_authenticated:
            print("You need to be authenticated to search and order items.")
            return

        while True:
            search_term = input(
                "Enter the item you want to search (or 'cancel' to go back): "
            ).strip()
            if search_term.lower() == "cancel":
                return

            found_items, item_counts = self.search_item(stock, search_term)
            if found_items:
                self.order_items(found_items, item_counts)
            else:
                print("Item not found.")

    def search_item(
        self, stock: List[Warehouse], search_term: str
    ) -> Tuple[List[Item], Counter]:
        found_items = []
        item_counts = Counter()

        for warehouse in stock:
            for item in warehouse.stock:
                if search_term.lower() in item.category.lower():
                    found_items.append(item)
                    item_key = (
                        f"{item.state} {item.category} (Warehouse {item.warehouse})"
                    )
                    item_counts[item_key] += 1
                    self.last_searched_item = item  # check

        return found_items, item_counts

    def order_items(self, found_items: List[Item], item_counts: Counter) -> None:
        if found_items:
            while True:
                print("Available items:")
                for i, item in enumerate(found_items, 1):
                    item_key = (
                        f"{item.state} {item.category} (Warehouse {item.warehouse})"
                    )
                    count = item_counts.get(item_key, 0)
                    date_str = item.date_of_stock
                    date_format = "%Y-%m-%d %H:%M:%S"
                    days = (
                        datetime.now() - datetime.strptime(date_str, date_format)
                    ).days

                    print(
                        f"{i}. {item_key}, Days in Stock: {days} days , Available: {count} pcs"
                    )

                item_choice = input(
                    "Enter the number of the item you want to order (or 'cancel' to go back): "
                ).strip()
                if item_choice == "cancel":
                    return  # Return to the main menu

                try:
                    item_choice = int(item_choice)
                    if 1 <= item_choice <= len(found_items):
                        selected_item = found_items[item_choice - 1]
                        item_key = f"{selected_item.state} {selected_item.category} (Warehouse {selected_item.warehouse})"
                        available_quantity = item_counts.get(item_key, 0)

                        print(
                            f"You have selected: {item_key}, Available: {available_quantity}"
                        )

                        while True:
                            order_quantity = input(
                                "Enter the quantity you want to order: "
                            ).strip()
                            if order_quantity.isdigit():
                                order_quantity = int(order_quantity)
                                if 1 <= order_quantity <= available_quantity:
                                    self.place_order(
                                        selected_item, order_quantity, item_counts
                                    )
                                    self.last_ordered_item = selected_item
                                    self.last_ordered_quantity = order_quantity
                                    return  # Return to the main menu
                                else:
                                    print(
                                        "Invalid quantity. Please enter a valid quantity."
                                    )
                            else:
                                print(
                                    "Invalid input. Please enter a number for quantity"
                                )
                    else:
                        print("Invalid item number. Please enter a valid item number")
                except ValueError:
                    print("Invalid input. Please enter a number for item selection")
        else:
            print("Item not found")

    def place_order(self, item: Item, quantity: int, item_counts: Counter) -> None:
        item_key = f"{item.state} {item.category} (Warehouse {item.warehouse})"
        available_quantity = item_counts[item_key]

        if quantity <= available_quantity:
            item_counts[item_key] -= quantity
            print(f"Order placed for {quantity} of '{item_key}'")
            self.last_ordered_item_state = item.state
            self.last_ordered_item_category = item.category
            self.last_ordered_quantity = quantity
        else:
            print("Not enough quantity available for the order.")


class SessionReport:
    def __init__(self, user: User):
        self.user = user
        self.actions = []
        self.items_searched = []
        self.items_browsed = []
        self.items_ordered = []

    def add_action(self, action: str) -> None:
        self.actions.append(action)

    def record_searched_item(self, item_name: str) -> None:
        self.items_searched.append(item_name)

    def record_browsed_item(self, item_name: str) -> None:
        self.items_browsed.append(item_name)

    def record_ordered_item(
        self, item_state: str, item_category: str, quantity: int
    ) -> None:
        self.items_ordered.append((item_state, item_category, quantity))

    def display_report(self) -> None:
        print(f"Thank you for your visit, {self.user._name}!")

        if self.actions:
            print("In this session, you have:")
            for i, action in enumerate(self.actions, 1):
                print(f"{i}. {action}")

            if self.items_searched:
                print("Items Searched:")
                for i, item_name in enumerate(self.items_searched, 1):
                    print(f"{i}. Searched for item: {item_name}")

            if self.items_browsed:
                print("Items Browsed:")
                for i, item_name in enumerate(self.items_browsed, 1):
                    print(f"{i}. Browsed item: {item_name}")

            if self.items_ordered:
                print("Items Ordered:")
                for i, (state, category, quantity) in enumerate(self.items_ordered, 1):
                    print(f"{i}. Ordered {quantity} of item: {state} {category}")
