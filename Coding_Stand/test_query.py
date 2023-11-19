"""
This code snippet is a unit test class called `TestQuery`.

that tests variousfunctions in the `query` module. It includes tests
for user authentication,selecting an operation, displaying warehouses,
and searching and ordering items.

Inputs:
- `mock_input`: A context manager that mocks the `input` function by replacing
it with a function that returns a specified value.
- `mock_output`: A context manager that mocks the `print` function by
replacing it with a function that appends the printed values to a list.
- `personnel_data`: A list of `Employee` objects representing employee data.
- `stock`: A list of `Warehouse` objects representing the stock of items in
different warehouses.
- `search_item`: A string representing the item to search for.

Outputs:
- `user_obj`: An instance of the `User` or `Employee` class representing the
authenticated user.
- `result`: A string representing the selected operation choice.
- `prints`: A list of strings representing the printed output.

Example Usage:
- Test guest login by mocking the input function to return a guest name.
Assert that the returned object is an instance of the `User` class.
- Test employee authentication by mocking the input function to return an
employee name and password. Assert that the returned object is an instance of
the `Employee` class and that the `is_authenticated` attribute is True.
- Test selecting an operation by mocking the input function to return a valid
choice. Assert that the returned value matches the input choice.
- Test displaying warehouses by mocking the output function and capturing the
printed output. Assert that the printed output matches the expected output.
- Test searching and ordering items by mocking the input function to return a
search term and capturing the printed output. Assert that the number of found
items matches the sum of item counts.
"""
import unittest
from contextlib import contextmanager
from unittest.mock import patch

import query
from classes import Employee, User, WarehouseManager
from query import stock


@contextmanager
def mock_input(mock):
    """
    Contex manager that mocks the `input` function by replacing it with a.

    function that returns a specified value.

    Args:
    - mock: A value that will be returned by the mocked `input` function.

    Returns:
    None. The function is used as a context manager to
    mock the `input` function.
    """
    original_input = __builtins__.input
    __builtins__.input = lambda _: mock
    yield
    __builtins__.input = original_input


@contextmanager
def mock_output(mock):
    """
    Context manager that mocks the print function by replacing.

    it with a function that appends the printed values to a list.

    :param mock: A list that will be used to store the printed values.
    :type mock: list
    """
    original_print = __builtins__.print
    __builtins__.print = lambda *value: [mock.append(val) for val in value]
    yield
    __builtins__.print = original_print


class TestQuery(unittest.TestCase):
    """
    This class contains unit tests for the functions in the query module.

    It tests the user authentication process, the selection of operations,
    the display of warehouses, and the search and order functionality.
    """

    def test_user_authentication_guest_mode(self):
        """
        Tests the guest login functionality by mocking the input and asserting.

        that the returned object is an instance of the User class.
        """
        with mock_input("Bishi"):
            user_obj = query.guest_login()
            self.assertIsInstance(user_obj, User)
            print(f" User obj : {(user_obj)}, User: {(User)}")

    @patch("builtins.input", side_effect=["Jeremy", "coppers"])
    def test_user_authentication_employee_mode(self, mock_input):
        """
        Tests the employee authentication functionality by mocking the input.

        and asserting that the returned object is an instance of the Employee
        class and that the is_authenticated attribute is set to True.
        """
        personnel_data = [
            Employee(user_name="Jeremy", password="coppers"),
        ]

        with mock_input:
            user_obj = query.get_authenticated_user(personnel_data)

        self.assertIsInstance(user_obj, Employee)

        # The 'is_authenticated' attribute is part of the User class
        self.assertTrue(user_obj.is_authenticated)

        print(f" User obj : {(user_obj)}, User: {(Employee)}")
        print(f" User obj : {(user_obj.is_authenticated)}, User: {(True)}")

    def test_get_selected_operation_valid_input(self):
        """
        Tests the selection of operations functionality by mocking the input.

        and asserting that the returned choice is valid.
        """
        with mock_input("1"):
            prints = []
            with mock_output(prints):
                result = query.get_selected_operation()
            self.assertEqual(result, "1")
        expected_output = [
            "1. Display Warehouses",
            "2. Search and Order Item",
            "3. Browse by Category",
            "4. Exit",
        ]

        self.assertEqual(expected_output, prints)
        print(f"Expected output {expected_output}")
        print(f"Actual output {prints}")

    def test_item_list_by_warehouse(self):
        """
        Tests the display of warehouses functionality by asserting that the.

        total item count from all warehouses is correct.
        """
        prints = []
        with mock_output(prints):
            wh = WarehouseManager(stock)
            _ = wh.display_warehouses()
            total_item_count = 0

        for warehouse in stock:
            stock_count = warehouse.occupancy()
            total_item_count += stock_count

        self.assertEqual(
            total_item_count,
            5000,
            "Incorrect the total items from all warehouse are 5000",
        )
        print(f"Total Items: {total_item_count}")

    def test_search_and_order(self):
        """
        Tests the search and order functionality by mocking the input.

        and output, and asserting that the number of found items
        matches the sum of item counts.
        """
        search_item = "Monitor"

        prints = []
        with mock_input(search_item), mock_output(prints):
            employee_instance = Employee()

        found_items, item_counts = employee_instance.search_item(
            stock, search_item
        )

        self.assertEqual(
            len(found_items),
            sum(item_counts.values()),
            "The search items list is not matching",
        )
        print(f"Found Items : {len(found_items)}")
        print(f"Sum of item counts :  {sum(item_counts.values())}")


if __name__ == "__main__":
    unittest.main()
