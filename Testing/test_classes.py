from classes import User, Employee, Warehouse, Item
import unittest


class TestClasses(unittest.TestCase):
    def test_class_existence(self):
        classes = __import__("classes")
        user_exists = hasattr(classes, "User")
        employee_exists = hasattr(classes, "Employee")
        warehouse_exists = hasattr(classes, "Warehouse")
        item_exists = hasattr(classes, "Item")
        self.assertTrue(user_exists)
        self.assertTrue(employee_exists)
        self.assertTrue(warehouse_exists)
        self.assertTrue(item_exists)

    def test_inheritance(self):
        self.assertTrue(issubclass(Employee, User))

    def test_user_creation(self):
        # user without name
        user_without_name = User()
        self.assertEqual(
            user_without_name._name,
            "Anonymous",
            "User should be Anonymous as no name provided",
        )
        user_without_name.authenticate("AnonymousPassword")
        self.assertEqual(
            user_without_name.is_authenticated, False, "Authentication should be False"
        )

        # User with name
        user_with_name = User("JohnDoe")
        self.assertEqual(user_with_name._name, "JohnDoe", "User name should be JohnDoe")
        user_with_name.authenticate("JohnDoePassword")
        self.assertEqual(
            user_with_name.is_authenticated, False, "Authentication should be False"
        )

        # user with name and password
        user_with_password = User("JaneSmith", "JanePassword")
        self.assertEqual(
            user_with_password._name,
            "JaneSmith",
            "User name should be JaneSmith with password=JanePassword",
        )
        user_with_password.authenticate("JanePassword")
        self.assertEqual(
            user_with_password.is_authenticated, True, "Authentication should be False"
        )

    def test_item_properties_and_representation(self):
        # Create an example Item instance
        example_item = Item(
            state="New",
            category="Monitor",
            warehouse=2,
            date_of_stock="2022-07-23 20:10:11",
        )

        # Check if the properties of the Item object match the expected values
        expected_properties = ["New", "Monitor", "2022-07-23 20:10:11"]
        self.assertEqual(
            [example_item.state, example_item.category, example_item.date_of_stock],
            expected_properties,
            "Item properties are not stored properly",
        )

        # Check if the string representation is correct
        expected_representation = f"{example_item.state} {example_item.category}"
        self.assertEqual(
            str(example_item),
            expected_representation,
            "String representation of the Item object is incorrect",
        )


class TestEmployee(unittest.TestCase):
    def test_employee_authentication_and_head_of(self):
        # Employee without name and password
        employee1 = Employee()
        self.assertEqual(
            employee1.is_authenticated,
            False,
            "Employee without name and password should not be authenticated",
        )
        self.assertEqual(
            employee1.head_of, [], "Head of should be empty for an unknown employee"
        )

        # Employee with a name, password, and authentication
        employee2 = Employee(user_name="JohnDoe", password="password123", head_of=[])
        employee2.authenticate("password123")
        self.assertTrue(
            employee2.is_authenticated,
            "Employee with correct password should be authenticated",
        )
        self.assertEqual(
            employee2.head_of,
            [],
            "Head of should not be set for employee without head_of information",
        )

        # Employee with a name, password, and head_of
        head_of_info = [{"user_name": "Alice", "password": "alice123", "head_of": []}]
        employee3 = Employee(user_name="Bob", password="bob567", head_of=head_of_info)
        employee3.authenticate("bob567")
        self.assertTrue(
            employee3.is_authenticated,
            "Employee with correct password should be authenticated",
        )
        self.assertTrue(
            employee3.head_of,
            "Head of should be set for employee with head_of information",
        )
        self.assertIsInstance(employee3.head_of, list, "Head of should be a list")

        for other_employee in employee3.head_of:
            self.assertIsInstance(
                other_employee,
                Employee,
                "Elements in head_of should be instances of Employee",
            )

    def test_warehouse_properties_and_methods(self):
        # Test Warehouse object creation without parameters
        warehouse_without_id = Warehouse()
        self.assertEqual(
            warehouse_without_id.id,
            None,
            "Warehouse object without parameter should set id to None",
        )

        # Test Warehouse object creation with id parameter
        warehouse_with_id = Warehouse(1)
        self.assertEqual(
            warehouse_with_id.id,
            1,
            "Warehouse object with parameter 1 should set id to 1",
        )

        # Check default stock property
        self.assertEqual(
            warehouse_with_id.stock,
            [],
            "Default stock property should be an empty list",
        )
        self.assertEqual(
            type(warehouse_with_id.stock),
            list,
            "Default stock property should be a list",
        )

        # Check initial occupancy method
        initial_stock_len = len(warehouse_with_id.stock)
        self.assertEqual(
            warehouse_with_id.occupancy(),
            initial_stock_len,
            "Occupancy method should return the length of the initial stock list",
        )

        # Create example items
        item1 = Item(
            state="Blue",
            category="Mouse",
            warehouse=2,
            date_of_stock="2021-05-26 17:20:10",
        )
        item2 = Item(
            state="Red",
            category="Mouse",
            warehouse=1,
            date_of_stock="2021-05-26 17:20:10",
        )

        # Add items to the warehouse and check updated occupancy
        warehouse_with_id.add_item(item1)
        warehouse_with_id.add_item(item2)
        updated_stock_len = initial_stock_len + 2
        self.assertEqual(
            warehouse_with_id.occupancy(),
            updated_stock_len,
            "Occupancy method should return the updated length of the stock list",
        )

    def test_Employee_search_item(self):
        # Assuming you have Employee and Warehouse instances
        employee = Employee()
        warehouse1 = Warehouse(1)
        warehouse2 = Warehouse(2)

        # Add some items to the warehouses
        item1 = Item(
            state="Blue",
            category="Mouse",
            warehouse=1,
            date_of_stock="2021-05-26 17:20:10",
        )
        item2 = Item(
            state="Red",
            category="Mouse",
            warehouse=1,
            date_of_stock="2021-05-26 17:20:10",
        )
        item3 = Item(
            state="Orange",
            category="Keyboard",
            warehouse=2,
            date_of_stock="2021-05-26 17:20:10",
        )

        warehouse1.add_item(item1)
        warehouse1.add_item(item2)
        warehouse2.add_item(item3)

        stock = [warehouse1, warehouse2]

        # Perform a search using the search_item method
        search_term = "Mouse"
        found_items, item_counts = employee.search_item(stock, search_term)

        # Assert the results based on your expectations
        self.assertEqual(
            len(found_items), 2, "Expected 2 items matching the search term"
        )
        self.assertEqual(
            item_counts["Blue Mouse (Warehouse 1)"],
            1,
            "Expected 1 occurrence of Blue Mouse in Warehouse 1",
        )
        self.assertEqual(
            item_counts["Red Mouse (Warehouse 1)"],
            1,
            "Expected 1 occurrence of Red Mouse in Warehouse 1",
        )

        # Perform another search
        search_term = "Keyboard"
        found_items, item_counts = employee.search_item(stock, search_term)

        # Assert the results based on your expectations
        self.assertEqual(
            len(found_items), 1, "Expected 1 item matching the search term"
        )
        self.assertEqual(
            item_counts["Orange Keyboard (Warehouse 2)"],
            1,
            "Expected 1 occurrence of Orange Keyboard in Warehouse 2",
        )


if __name__ == "__main__":
    unittest.main()
