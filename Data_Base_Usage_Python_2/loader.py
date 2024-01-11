#loader.py
import json
import os
import psycopg2
from classes import Item, Employee

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
EMPLOYEES_PATH = os.path.join(BASE_DIR, "data", "personnel.json")
STOCK_PATH = os.path.join(BASE_DIR, "data", "stock.json")

employees = []
items = []

DATABASE_CONFIG = {
    "dbname": "wh-project",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
    "port": "5432",
}

# Load items from the database
with psycopg2.connect(**DATABASE_CONFIG) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM item")
        items_data = cursor.fetchall()

items = [Item(*item) for item in items_data]

with psycopg2.connect(**DATABASE_CONFIG) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT employee_id, user_name, password, head_of FROM employee")
        employees_data = cursor.fetchall()

employees = [Employee(*employee) for employee in employees_data]

def _import(name):
    """Dynamically import a package."""
    try:
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
    except Exception:
        mod = None
    return mod

class MissingClassError(Exception):
    """Missing class exception."""

    def __init__(self, name=None, message="Missing class"):
        """Construct object."""
        self.class_name = name
        self.message = f"Missing class {name}."
        super().__init__(self.message)

class Loader:
    """Main data loader class."""

    model = None
    objects = None

    def __init__(self, *args, **kwargs):
        """Construct object."""
        if "model" not in kwargs:
            raise Exception("The loader requires a `model` "
                            "keyword argument to work.")
        self.model = kwargs["model"]
        self.parse()

    def parse(self):
        """Instantiate objects from the data."""
        if self.model == "personnel":
            self.objects = self.__parse_personnel()
        if self.model == "stock":
            self.objects = self.__parse_stock()

    def __load_class(self, name):
        """Return a class."""
        classes = _import("classes")
        if not hasattr(classes, name):
            raise MissingClassError(name)
        return getattr(classes, name)

    def __parse_personnel(self):
        """Parse the personnel list."""
        Employee = self.__load_class("Employee")  # noqa: N806

        employees = []
        for employee_data in employees_data:
            employee_id, user_name, password, head_of_data = employee_data
            head_of = [Employee(user_name=user_name, password=password, employee_id=head_id) for head_id in [head_of_data]] if head_of_data else []
            
            employee = Employee(employee_id=employee_id, user_name=user_name, password=password, head_of=head_of)
            employees.append(employee)

        return employees
    
    def __parse_stock(self):
        """Parse the stock."""
        Item = self.__load_class("Item")  # noqa: N806
        Warehouse = self.__load_class("Warehouse")  # noqa: N806

        warehouses = {}
        for item_data in items_data:
            item_id, state, category, warehouse, date_of_stock = item_data
            warehouse_id_str = str(warehouse) if warehouse else "unknown"
            
            if warehouse_id_str not in warehouses.keys():
                warehouses[warehouse_id_str] = Warehouse(warehouse_id_str)
            
            item = Item(item_id=item_id, state=state, category=category, warehouse=warehouse, date_of_stock=date_of_stock)
            warehouses[warehouse_id_str].add_item(item)

        return list(warehouses.values())

    def __iter__(self, *args, **kwargs):
        """Iterate through the objects."""
        yield from self.objects

    def to_dict(self):
        """Return a dictionary."""
        data = None
        if self.model == "stock":
            data = []
            for warehouse in self.objects:
                for item in warehouse.stock:
                    item_dict = vars(item)
                    item_dict["warehouse"] = warehouse.id
                    data.append(item_dict)
        return data