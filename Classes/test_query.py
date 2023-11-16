import unittest
from unittest.mock import patch
from contextlib import contextmanager
from classes import User, Employee, Warehouse,Item,WarehouseManager
import query
from query import stock

@contextmanager
def mock_input(mock):
    original_input = __builtins__.input
    __builtins__.input = lambda _: mock
    yield 
    __builtins__.input = original_input


@contextmanager
def mock_output(mock):
    original_print = __builtins__.print
    __builtins__.print = lambda *value: [mock.append(val) for val in value]
    yield
    __builtins__.print = original_print

class TestQuery(unittest.TestCase):

    def test_user_authentication_guest_mode(self):
        with mock_input("Bishi"):
            user_obj = query.guest_login()
            self.assertIsInstance(user_obj, User)
            print(f" User obj : {(user_obj)}, User: {(User)}")
            
            
    
    @patch('builtins.input', side_effect=["Jeremy", "coppers"])
    def test_user_authentication_employee_mode(self, mock_input):
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
        with mock_input("1"):
            prints =[]
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
        
        
    def test_item_list_by_Warehouse(self):
        prints=[]
        with mock_output(prints):
            wh=WarehouseManager(stock)
            items=wh.display_warehouses()
            total_item_count = 0
        
        for warehouse in stock:
            stock_count = warehouse.occupancy()
            total_item_count += stock_count
            
        self.assertEqual(total_item_count,5000,"Incorrect the total items from all warehouse are 5000")
        print(f"Total Items: {total_item_count}")
        
        
        
    def test_search_and_order(self):
        search_item = "Monitor"
        
        prints = []
        with mock_input(search_item), mock_output(prints):
            employee_instance = Employee()

        found_items, item_counts = employee_instance.search_item(stock, search_item)

        self.assertEqual(len(found_items), sum(item_counts.values()), "The search items list is not matching")
        print(f"Found Items : {len(found_items)}")
        print(f"Sum of item counts :  {sum(item_counts.values())}")
        
if __name__ == "__main__":
    unittest.main()
        
    