--отсортировать по required_date (по убыванию) и отсортировать по дате отгрузке (по возрастанию)
SELECT required_date, shipped_date   
FROM orders
ORDER BY required_date DESC, shipped_date ASC

-- среднее значение дней уходящих на доставку с даты формирования заказа в USA
SELECT AVG(date_part('day',age(o.required_date, o.shipped_date)))
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE c.country = 'USA' 

--сумма на которую имеется товаров
SELECT  SUM(p.unit_price * p.units_in_stock)
FROM products p
WHERE p.discontinued = 0


