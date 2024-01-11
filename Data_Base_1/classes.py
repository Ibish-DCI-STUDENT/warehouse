#classes.py
from collections import Counter
from datetime import datetime
from typing import List, Tuple
import json
import os


class MissingArgument(Exception):
    def __init__(self, argument, message):
        self.argument = argument
        self.message = message
        super().__init__(f"stock.classes.MissingArgument: {argument} is missing. {message}")

class ItemNotFoundError(Exception):
    def __init__(self, item_name):
        self.item_name = item_name
        super().__init__(f"stock.classes.ItemNotFoundError: Item '{item_name}' not found.")

class InsufficientQuantityError(Exception):
    def __init__(self, item_name, requested_quantity, available_quantity):
        self.item_name = item_name
        self.requested_quantity = requested_quantity
        self.available_quantity = available_quantity
        super().__init__(f"stock.classes.InsufficientQuantityError: "
                         f"Requested {requested_quantity} of item '{item_name}', "
                         f"but only {available_quantity} available.")

class NoResultsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f"stock.classes.NoResultsError: {message}")
        
        
class Item:
    def __init__(self, state, category, warehouse, date_of_stock):
        self.state = state
        self.category = category
        self.warehouse = warehouse
        self.date_of_stock = date_of_stock
        self.sold = False  # New attribute to track if the item has been sold
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

    def __str__(self) -> str:
        return f"Warehouse {self.id}"

    def search(self, search_term: str) -> List[Item]:
        return [
            item
            for item in self.stock
            if search_term.lower() in item.category.lower()
        ]

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
            "If you don't find what you are looking for,"
            "please ask one of our staff members to assist you."
        )

    def employee_greet(self):
        print(
            "\nIf you experience a problem with the system, "
            "\nPlease contact technical support."
        )

    def display_warehouses(self, stock: List[Warehouse]) -> str:
        total_item_count = 0

        for warehouse in stock:
            stock_count = warehouse.occupancy()
            total_item_count += stock_count

            print(f"Warehouse {warehouse.id} - Stock Count: {stock_count}")

        print(f"Listed {total_item_count} items.")
    
    
        
    # def list_all_items(self, stock):
    #     """List all items across warehouses."""
    #     print("All Items Across Warehouses:")
    #     for warehouse in stock:
    #         print(f"Warehouse{warehouse.id}")
            


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
                "Type the number of the category to browse "
                "(or 'cancel' to go back): "
            )
            .strip()
            .lower()
        )
        if choice == "cancel":
            return

        try:
            category_choice = int(choice)
            if 1 <= category_choice <= len(categories):
                selected_category = list(categories.keys())[
                    category_choice - 1]

                self.last_browsed_item = selected_category
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
                        f"{item.state} ({
                            item.category}) - Stocked on: {item.date_of_stock}"
                    )
            else:
                print("Invalid category number. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
class Employee(User):
    def __init__(self, user_name=None, password=None, **kwargs):
        super().__init__(user_name, password)
        if user_name is None:
            raise MissingArgument("user_name", "An employee cannot be anonymous.")
        if password is None:
            raise MissingArgument("password", "An employee requires authentication.")
        
        self.password = password
        
        self.head_of = [Employee(**employee) for employee in kwargs.get("head_of", [])]
        self.last_searched_item = self.last_browsed_item = None
        self.last_browsed_quantity = self.last_ordered_item = None
        self.last_ordered_quantity = self.last_ordered_item_state = None
        self.last_ordered_item_category = self.displayed_warehouse = None

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
                self.order_items(found_items, item_counts, stock)

            else:
                print("Item not found.")

    def search_item(
        self, stock: List[Warehouse], search_term: str) -> Tuple[List[Item], Counter]:

        found_items = []
        item_counts = Counter()

        for warehouse in stock:
            for item in warehouse.stock:
                if search_term.lower() in item.category.lower():
                    found_items.append(item)
                    item_key = (
                        f"{item.state} {item.category} (Warehouse {
                            item.warehouse})"
                    )
                    item_counts[item_key] += 1
                    self.last_searched_item = item

        return found_items, item_counts

    def order_items(self, found_items: List[Item], item_counts: Counter, stock: List[Warehouse]):
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
                            datetime.now() -
                            datetime.strptime(date_str, date_format)
                        ).days

                    print(
                        f"{i}. {item_key}, Days in Stock: {days} days ,Available: {count} pcs"
                    )

                item_choice = input(
                    "Enter the number of the item you want to order"
                    "(or 'cancel' to go back): "
                ).strip()
                if item_choice == "cancel":
                    return  # Return to the main menu

                try:
                    item_choice = int(item_choice)
                    if 1 <= item_choice <= len(found_items):
                        selected_item = found_items[item_choice - 1]
                        item_key = (
                            f"{selected_item.state} "
                            f"{selected_item.category} "
                            f"(Warehouse {selected_item.warehouse})"
                        )
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
                                    # Pass the stock to the place_order method
                                    self.place_order(selected_item, order_quantity, item_counts, stock)
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

    def place_order(self, item: Item, quantity: int, item_counts: Counter, stock: List[Warehouse]):
        item_key = f"{item.state} {item.category} (Warehouse {item.warehouse})"
        available_quantity = item_counts[item_key]

        if quantity <= available_quantity:
            item_counts[item_key] -= quantity

            # Find the corresponding item in the warehouse and update its quantity
            for warehouse in stock:
                for warehouse_item in warehouse.stock:
                    if (
                        warehouse_item.state == item.state
                        and warehouse_item.category == item.category
                        and warehouse_item.warehouse == item.warehouse
                    ):
                        warehouse_item_key = (
                            f"{warehouse_item.state} {warehouse_item.category} "
                            f"(Warehouse {warehouse_item.warehouse})"
                        )
                        item_counts[warehouse_item_key] -= quantity
                        break

            print(f"Order placed for {quantity} of '{item_key}'")
            self.last_ordered_item_state = item.state
            self.last_ordered_item_category = item.category
            self.last_ordered_quantity = quantity
        else:
            print("Not enough quantity available for the order.")



class SessionReport:
    """
    A class to keep track of the actions performed by a user.

    Attributes:
        user (User): The user object associated with the session report.
        actions (list): A list of actions performed during the session.
        items_searched (list): A list of searched items during the session.
        items_browsed (list): A list of browsed items during the session.
        items_ordered (list): A list of ordered items during the session.
    """

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
                for i, (state, category, quantity) in enumerate(
                    self.items_ordered, 1
                ):
                    print(
                        f"{i}. Ordered {quantity} of item: "
                        f"{state} {category}"
                    )

    def save_to_log(self) -> None:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        if self.user.is_authenticated:
            filename = "log/employee_log.txt"
        else:
            filename = "log/user_log.txt"

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "a") as log_file:
            log_file.write(f"Session Report for {self.user._name}:\n")

            if self.items_searched:
                log_file.write("Items Searched:\n")
                for i, item_name in enumerate(self.items_searched, 1):
                    log_file.write(f" {i}. Searched for item: {item_name} - {current_datetime}\n")

            if self.items_browsed:
                log_file.write("Items Browsed:\n")
                for i, item_name in enumerate(self.items_browsed, 1):
                    log_file.write(f" {i}. Browsed item: {item_name} - {current_datetime}\n")

            if self.items_ordered:
                log_file.write("Items Ordered:\n")
                for i, (state, category, quantity) in enumerate(self.items_ordered, 1):
                    log_file.write(
                        f" {i}. Ordered {quantity} of item: {state} {category} - {current_datetime}\n"
                    )

            log_file.write(f"Actions performed:\n")
            for i, action in enumerate(self.actions, 1):
                log_file.write(f" {i}. {action} - {current_datetime}\n")

        print(f"Session report saved to {filename}")