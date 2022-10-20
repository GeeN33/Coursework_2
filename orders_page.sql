--отсортировать по required_date (по убыванию) и отсортировать по дате отгрузке (по возрастанию)
SELECT required_date, shipped_date   
FROM orders
ORDER BY required_date DESC, shipped_date ASC

-- среднее значение дней уходящих на доставку с даты формирования заказа в USA
SELECT AVG(o.shipped_date - o.order_date)
FROM orders o
WHERE o.ship_country = 'USA' 

--сумма на которую имеется товаров
SELECT  SUM(p.unit_price * p.units_in_stock)
FROM products p
WHERE p.discontinued = 0

SELECT *
FROM orders 


