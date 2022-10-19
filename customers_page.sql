--количество заказчиков
SELECT COUNT(*)
FROM customers

-- все уникальные сочетания 
SELECT DISTINCT c.city, c.country
FROM customers c

--заказчики и сотрудники из города London, и доставка идёт компанией Speedy Express
SELECT c.company_name , e.first_name, e.last_name
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN employees e ON e.employee_id = o.employee_id
JOIN shippers s ON  s.shipper_id = o.ship_via
WHERE c.city = 'London' AND e.city = 'London' AND s.company_name = 'Speedy Express'

--заказчики, не сделавших ни одного заказа
SELECT c.company_name, o.order_id 
FROM customers c
FULL JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL
