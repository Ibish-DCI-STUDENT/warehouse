-- Create the Employee table
CREATE TABLE Employee (
    employee_id SERIAL PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    head_of INT REFERENCES Employee(employee_id)
);


-- Create the Item table
CREATE TABLE Item (
    item_id SERIAL PRIMARY KEY,
    state VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    warehouse_id INT NOT NULL,
    date_of_stock DATE NOT NULL);

-- Create the Warehouse table
CREATE TABLE Warehouse (
    warehouse_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
