--записи работников в которых регион неизвестен
SELECT *
FROM employees
WHERE region IS NULL

-- страны в которых "зарегистированы" одновременно заказчики и поставщики, но при этом в них не "зарегистрированы" работники 
SELECT DISTINCT c.country
FROM customers c
WHERE (SELECT EXISTS (SELECT * FROM suppliers WHERE country = c.country))
AND NOT (SELECT EXISTS (SELECT * FROM employees WHERE country = c.country))


