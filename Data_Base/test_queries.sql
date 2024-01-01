SELECT * FROM item;


-- How many smartphones are there in stock?
SELECT COUNT(*) FROM item WHERE category ILIKE 'smartphone';

-- How many blue items are there in stock in warehouse 1?
SELECT COUNT(*) FROM item WHERE state ILIKE 'blue' AND warehouse_id = 1;

-- How many items are in stock in warehouse 1?
SELECT COUNT(*) FROM item WHERE warehouse_id = 1;



-- Show a list of all warehouses, with their name and the amount of items in stock. Sort the list by the amount of items.
SELECT
    w.name AS warehouse_name,
    COUNT(*) AS item_count
FROM
    Warehouse w
JOIN
    Item i ON w.warehouse_id = i.warehouse_id
GROUP BY
    w.warehouse_id
ORDER BY
    item_count DESC;

SELECT * FROM item;
