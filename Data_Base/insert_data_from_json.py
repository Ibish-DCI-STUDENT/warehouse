import json
import psycopg2
from datetime import datetime

# Read JSON data from the stock file
with open('data/stock.json') as json_file:
    stock_data = json.load(json_file)

# Read JSON data from the employee file
with open('data/personnel.json') as json_file:
    employee_data = json.load(json_file)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname='wh-project',
    user='postgres',
    password='admin',
    host='localhost',
    port='5432'
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Set to store unique warehouse IDs and names
unique_warehouses = set()

# Iterate over each JSON object and collect unique warehouses for stock data
for item in stock_data:
    warehouse_id = item.get('warehouse')
    unique_warehouses.add((warehouse_id, str(warehouse_id)))  # Assuming warehouse names are derived from warehouse IDs

# Iterate over unique warehouses and insert into the warehouse table for stock data
for warehouse_id, warehouse_name in unique_warehouses:
    # Define the SQL query for warehouse insertion
    warehouse_sql_query = """
        INSERT INTO warehouse (warehouse_id, name)
        VALUES (%s, %s)
        ON CONFLICT (warehouse_id) DO NOTHING;  -- To avoid duplicate entries based on warehouse_id
    """

    # Execute the SQL query with the warehouse data
    cursor.execute(warehouse_sql_query, (warehouse_id, warehouse_name))

# Commit the changes for stock data
conn.commit()

# Iterate over each JSON object and insert data into the item table for stock data
for item_data in stock_data:
    state = item_data['state']
    category = item_data['category']
    warehouse_id = item_data['warehouse']
    date_of_stock = datetime.strptime(item_data['date_of_stock'], '%Y-%m-%d %H:%M:%S')

    # Define the SQL query for item insertion
    item_sql_query = """
        INSERT INTO item (state, category, warehouse_id, date_of_stock)
        VALUES (%s, %s, %s, %s);
    """

    # Execute the SQL query with the item data
    cursor.execute(item_sql_query, (state, category, warehouse_id, date_of_stock))

# Commit the changes for item data
conn.commit()

# Set to store unique employee user names and passwords
unique_employees = set()

# Function to recursively insert employees and their hierarchy
def insert_employee(employee_data, head_of_id=None):
    user_name = employee_data['user_name']
    password = employee_data['password']

    # Define the SQL query for employee insertion
    sql_query = """
        INSERT INTO Employee (user_name, password, head_of)
        VALUES (%s, %s, %s)
        RETURNING employee_id;
    """

    # Execute the SQL query with the employee data
    cursor.execute(sql_query, (user_name, password, head_of_id))
    
    # Fetch the generated employee ID
    employee_id = cursor.fetchone()[0]

    # Recursively insert employees in the "head_of" hierarchy
    head_of_list = employee_data.get('head_of', [])
    for head_of_data in head_of_list:
        insert_employee(head_of_data, head_of_id=employee_id)

# Iterate over each JSON object and insert data into the Employee table
for employee_data_entry in employee_data:
    insert_employee(employee_data_entry)

# Commit the changes for employee data
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
