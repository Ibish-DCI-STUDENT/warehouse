"""
The code module defines several classes related to managing warehouses.

Classes:
    - Item
    - Warehouse
    - WarehouseManager
    - User
    - Employee
    - SessionReport

These classes have methods for:
    - Adding items to a warehouse
    - Searching for items
    - Browsing categories
    - Placing orders
    - Recording session actions
"""
from collections import Counter
from datetime import datetime
from typing import List, Tuple


# OK
class Item:
    """
    Represents an item in a warehouse.

    Attributes:
        state (str): The state of the item (e.g., "New", "Used").
        category (str): The category of the item
        (e.g., "Electronics", "Clothing").
        warehouse (int): The ID of the warehouse where the item is stocked.
        date_of_stock (str): The date when the item was stocked
        in the warehouse.
    """

    def __init__(self, state, category, warehouse, date_of_stock):
        """
        Initialize a new instance of the Item class.

        Args:
            state (str): The state of the item.
            category (str): The category of the item.
            warehouse (int): The ID of the warehouse where the item is stocked.
            date_of_stock (str): The date when the item was stocked in
            the warehouse.
        """
        self.state = state
        self.category = category
        self.warehouse = warehouse
        self.date_of_stock = date_of_stock

    def __str__(self):
        """
        Return a string representation of the item.

        Returns:
            str: The state and category of the item.
        """
        return f"{self.state} {self.category}"


class Warehouse:
    """
    Represents a warehouse and its stock of items.

    Attributes:
        id (int): The ID of the warehouse.
        stock (List[Item]): The list of items in the warehouse's stock.
    """

    def __init__(self, warehouse_id=None):
        """

        Initialize a new instance of the Warehouse class.

        Args:
            warehouse_id (int, optional): The ID of the warehouse.
            Defaults to None.
        """
        self.id = warehouse_id
        self.stock = []

    def occupancy(self) -> int:
        """
        Returnsthe number of items in the warehouse's stock.

        Returns:
            int: The number of items in the warehouse's stock.
        """
        return len(self.stock)

    def add_item(self, item: Item) -> None:
        """
        Add an item to the warehouse's stock.

        Args:
            item (Item): The item to be added to the warehouse's stock.
        """
        self.stock.append(item)

    def __str__(self) -> str:
        """
        Return a string representation of the warehouse.

        Returns:
            str: The string representation of the warehouse.
        """
        return f"Warehouse {self.id}"

    def search(self, search_term: str) -> List[Item]:
        """
        Search for items in the warehouse's stock based on a search term.

        Args:
            search_term (str): The search term to be used for searching items.

        Returns:
            List[Item]: The list of items that match the search term.
        """
        return [
            item
            for item in self.stock
            if search_term.lower() in item.category.lower()
        ]


class WarehouseManager:
    """
    A class for managing a list of warehouses and providing functionality.

    Attributes:
        stock (List[Warehouse]): A list of warehouses representing the stock
        managed by the WarehouseManager instance.
    """

    def __init__(self, stock: List[Warehouse]):
        """
        Initialize a new instance of the WarehouseManager.

        Args:
            stock (List[Warehouse]): A list of warehouses
            representing the stock.
        """
        self.stock = stock

    def display_warehouses(self) -> str:
        """
        Display information about the warehouses and their stock.

        Returns:
            str: A string with the total number of items listed.
        """
        total_item_count = 0

        for warehouse in self.stock:
            stock_count = warehouse.occupancy()
            total_item_count += stock_count

            print(f"Warehouse {warehouse.id} - Stock Count: {stock_count}")

        print(f"Listed {total_item_count} items.")
        return f"Listed {total_item_count} items."

    def __str__(self) -> str:
        """
        Return a string representation of the WarehouseManager instance.

        Returns:
            str: A string representation of the WarehouseManager instance.
        """
        return f"{self.state} {self.category}"


class User:
    """
    Represents a user in the warehouse system.

    Attributes:
        _name (str): The user's name.
        is_authenticated (bool): A boolean indicating if the user
        is authenticated.
        password: The user's password.

    Methods:
        __init__(self, user_name: str = "Anonymous", password=None):
        Initializes a new instance of the User class with an optional user
        name and password.
        authenticate(self, provided_password: str) -> None: Authenticates
        the user with a provided password.is_named(self, name: str) -> bool:
        Checks if the user's name matches
        the provided name.
        greet(self): Greets the user and provides a welcome message.
        employee_greet(self): Greets the user as an employee and provides
        a message for technical support.
        bye(self, actions: List[str] = None) -> None: Says goodbye to the user
        and displays session actions if provided.
        browse_by_category(self, stock: List[Warehouse]) -> None: Allows the
        user to browse items by category.
    """

    def __init__(self, user_name: str = "Anonymous", password=None):
        """
        Initialize a new instance of the User class with.

        an optional user name and password.

        Args:
            user_name (str, optional): The user's name.
            Defaults to "Anonymous".
            password (str, optional): The user's password.
            Defaults to None.
        """
        self._name = user_name
        self.is_authenticated = False
        self.password = password

    def authenticate(self, provided_password: str) -> None:
        """
        Authenticate the user with a provided password.

        Args:
            provided_password (str): The password provided by the user.

        Returns:
            None
        """
        if provided_password == self.password:
            self.is_authenticated = True

    def is_named(self, name: str) -> bool:
        """
        Check if the user's name matches the provided name.

        Args:
            name (str): The name to compare with the user's name.

        Returns:
            bool: True if the names match, False otherwise.
        """
        return name == self._name

    def greet(self):
        """
        Greets the user and provides a welcome message.

        Returns:
            None
        """
        if self._name:
            print(f"Hello, {self._name}!\nWelcome to our Warehouse.")
        else:
            print("Hello, Anonymous!\nWelcome to our Warehouse.")
        print(
            "If you don't find what you are looking for,"
            "please ask one of our staff members to assist you."
        )

    def employee_greet(self):
        """
        Greet the user as an employee and provides a message.

        Returns:
            None
        """
        print(
            "\nIf you experience a problem with the system, "
            "\nPlease contact technical support."
        )

    def bye(self, actions: List[str] = None) -> None:
        """
        Says goodbye to the user and displays session actions if provided.

        Args:
            actions (List[str], optional): A list of session actions
            to display.
            Defaults to None.

        Returns:
            None
        """
        if actions:
            print(f"Thank you for your visit, {self._name}!")
            print("Session Actions:")
            for action in actions:
                print(action)
        else:
            print(f"Thank you for your visit, {self._name}!")

    def browse_by_category(self, stock: List[Warehouse]) -> None:
        """
        Allow the user to browse items by category.

        Args:
            stock (List[Warehouse]): A list of warehouses containing items.

        Returns:
            None
        """
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
    """
    A class representing an employee.

    Args:
        user_name (str, optional): The user name of the employee.
        password (str, optional): The password of the employee.
        **kwargs (optional): Additional keyword arguments.

    Attributes:
        password (str): The password of the employee.
        head_of (list): A list of employees that the
        current employee is the head of.

    Example:
        employee = Employee(user_name="John", password="password",
        head_of=[{"user_name": "Manager1", "password": "123456"},
        {"user_name": "Manager2", "password": "abcdef"}])
    """

    def __init__(self, user_name=None, password=None, **kwargs):
        """
        Initialize an Employee object with the provided user_name, password.

        Args:
            user_name (str, optional): The user name of the employee.
            password (str, optional): The password of the employee.
            **kwargs (dict, optional): Additional keyword arguments.

        Attributes:
            password (str): The password of the employee.
            head_of (list): A list of Employee objects representing employees
            that the current employee is the head of.
            last_searched_item (None): The last item searched by the employee.
            last_browsed_item (None): The last item browsed by the employee.

        Example:
            employee = Employee(user_name="John", password="password",
            head_of=[{"user_name": "Manager1", "password": "123456"},
            {"user_name": "Manager2", "password": "abcdef"}])

        """
        super().__init__(user_name, password)
        self.password = password
        if "head_of" in kwargs:
            self.head_of = [Employee(**employee)
                            for employee in kwargs["head_of"]]
        else:
            self.head_of = []

        # Initialize attributes for the last searched,
        # browsed, and ordered items
        self.last_searched_item = None
        self.last_browsed_item = None
        self.last_browsed_quantity = None
        self.last_ordered_item = None  # Updated to None initially
        self.last_ordered_quantity = None
        self.last_ordered_item_state = None  # New attributes
        self.last_ordered_item_category = None

    def search_and_order_item(self, stock: List[Warehouse]) -> None:
        """
        Allow an authenticated employee to search for items.

        Args:
            stock (List[Warehouse]): A list of Warehouse objects representing
            the stock of items in different warehouses.

        Returns:
            None: The method does not return any value. It either returns
            or continues the loop until the employee cancels
            the search and order process.
        """
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
        """
        Search for items in a list of warehouses  on a given search term.

        Args:
            stock (List[Warehouse]): A list of Warehouse objects representing
            the stock of items in different warehouses.
            search_term (str): The search term to be used for searching items.

        Returns:
            Tuple[List[Item], Counter]: A tuple containing a list of found
            items and a counter of item counts.
        """
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

    def order_items(self, found_items: List[Item], item_counts: Counter):
        """
        Allow an authenticated employee to select and order.

        Args:
            found_items (List[Item]):
            A list of items that match the search term.
            item_counts (Counter):
            A counter object that stores the count of each item.

        Returns:
            None

        Raises:
            ValueError: If the input for item selection or quantity is invalid.

        Example Usage:
            employee = Employee(user_name="John", password="password",
            head_of=[{"user_name": "Manager1", "password": "123456"},
            {"user_name": "Manager2", "password": "abcdef"}])
            employee.search_and_order_item(stock)
        """
        if found_items:
            while True:
                print("Available items:")
                for i, item in enumerate(found_items, 1):
                    item_key = (
                        f"{item.state} {item.category} (Warehouse {
                            item.warehouse})"
                    )
                    count = item_counts.get(item_key, 0)
                    date_str = item.date_of_stock
                    date_format = "%Y-%m-%d %H:%M:%S"
                    days = (
                            datetime.now() -
                            datetime.strptime(date_str, date_format)
                        ).days

                    print(
                        f"{i}. {item_key}, Days in Stock: {
                            days} days ,Available: {count} pcs"
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
                            f"You have selected: {item_key}, Available: {
                                available_quantity}"
                        )

                        while True:
                            order_quantity = input(
                                "Enter the quantity you want to order: "
                            ).strip()
                            if order_quantity.isdigit():
                                order_quantity = int(order_quantity)
                                if 1 <= order_quantity <= available_quantity:
                                    self.place_order(selected_item,
                                                     order_quantity,
                                                     item_counts
                                                     )
                                    self.last_ordered_item = selected_item
                                    self.last_ordered_quantity = order_quantity
                                    return  # Return to the main menu
                                else:
                                    print(
                                        "Invalid quantity."
                                        "Please enter a valid quantity."
                                    )
                            else:
                                print(
                                    "Invalid input. "
                                    "Please enter a number for quantity"
                                )
                    else:
                        print("Invalid item number. "
                              "Please enter a valid item number")
                except ValueError:
                    print("Invalid input."
                          "Please enter a number for item selection")
        else:
            print("Item not found")

    def place_order(self, item: Item, quantity: int, item_counts: Counter):
        """
        Place an order for a selected item.

        Args:
            item (Item): The item object representing the selected
            item to be ordered.
            quantity (int): The quantity of the item to be ordered.
            item_counts (Counter): A counter object that stores
            the count of each item.

        Returns:
            None

        Raises:
            None

        Example:
            employee = Employee(user_name="John", password="password",
            head_of=[{"user_name": "Manager1", "password": "123456"},
            {"user_name": "Manager2", "password": "abcdef"}])
            employee.place_order(item, quantity, item_counts)

        """
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
    """
    A class to keep track of the actions performed by a user.

    Attributes:
        user (User): The user object associated with the session report.
        actions (list): A list of actions performed during the session.
        items_searched (list): A list of searched items during the session.
        items_browsed (list): A list of browsed items during the session.
        items_ordered (list): A list of ordered items during the session.
    """

    def __init__(self, user: User):
        """
        Initialize a new instance of the SessionReport class.

        Args:
            user (User): The user object associated with the session report.
        """
        self.user = user
        self.actions = []
        self.items_searched = []
        self.items_browsed = []
        self.items_ordered = []

    def add_action(self, action: str) -> None:
        """
        Add an action to the list of actions performed during the session.

        Args:
            action (str): The action to be added.
        """
        self.actions.append(action)

    def record_searched_item(self, item_name: str) -> None:
        """
        Record a searched item during the session.

        Args:
            item_name (str): The name of the searched item.
        """
        self.items_searched.append(item_name)

    def record_browsed_item(self, item_name: str) -> None:
        """
        Record a browsed item during the session.

        Args:
            item_name (str): The name of the browsed item.
        """
        self.items_browsed.append(item_name)

    def record_ordered_item(
        self, item_state: str, item_category: str, quantity: int
    ) -> None:
        """
        Record an ordered item during the session.

        Args:
            item_state (str): The state of the ordered item.
            item_category (str): The category of the ordered item.
            quantity (int): The quantity of the ordered item.
        """
        self.items_ordered.append((item_state, item_category, quantity))

    def display_report(self) -> None:
        """Display a report of the session, including the actions."""
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
                for i, (state, category, quantity) in enumerate(
                        self.items_ordered, 1
                        ):

                    print(
                        f"{i}. Ordered {quantity} of item: "
                        f"{state} {category}"
                    )
