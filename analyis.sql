-- Zadanie 1
SELECT name, experience_years
FROM drivers
WHERE experience_years > 5
ORDER BY experience_years DESC;

-- Zadanie 2
SELECT AVG(salary) AS average_salary
FROM drivers;

-- Zadanie 3
SELECT vehicle_id, type, fuel_consumption_l_100km
FROM vehicles
ORDER BY fuel_consumption_l_100km DESC
LIMIT 3;

-- Zadanie 4
SELECT status, COUNT(*) as shipments_count
FROM shipments
GROUP BY status;

SELECT d.name, COUNT(s.shipment_id) as total_shipments
FROM drivers d
LEFT JOIN shipments s ON d.driver_id = s.driver_id
GROUP BY d.name
ORDER BY total_shipments DESC;
