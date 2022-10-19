--Найти активные (см. поле discontinued) продукты из категории Beverages и Seafood
SELECT p.product_name, p.units_in_stock, s.contact, s.phone
FROM products p
JOIN categories c ON c.category_id = p.category_id
JOIN suppliers s ON s.id = p.fk_suppliers
WHERE p.discontinued = 0 AND p.units_in_stock > 20 
AND c.category_name IN ('Beverages','Seafood') 


