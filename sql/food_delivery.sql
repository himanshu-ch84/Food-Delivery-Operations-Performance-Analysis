use food_delivery_app;

-- Q1. What are the top 3 delivery persons in each city based on average delivery performance, 
-- considering only delivery persons with a minimum number of orders?
WITH delivery_person_rnk AS
(
SELECT delivery_person_id, city,
       ROUND(AVG(delivery_person_rating),2) as avg_performance,
	  DENSE_RANK() OVER(PARTITION BY city ORDER BY AVG(delivery_person_rating) DESC) AS dr
FROM zomato
GROUP BY delivery_person_id, city
HAVING count(*) >= 5
)
SELECT delivery_person_id, avg_performance,city, dr
FROM delivery_person_rnk
WHERE dr <= 3
order by city, dr;

-- Q2. Which delivery persons show the greatest improvement in delivery performance
--  from one month to the next?
WITH performance_change AS
(SELECT delivery_person_id, DATE_FORMAT(order_date,'%Y-%m') AS month,
      ROUND(LAG(AVG(delivery_person_rating)) OVER(PARTITION BY delivery_person_id 
      ORDER BY DATE_FORMAT(order_date,'%Y-%m')),2) AS previous_performance,
      ROUND(AVG(delivery_person_rating),2) AS current_performance
FROM zomato
GROUP BY delivery_person_id, DATE_FORMAT(order_date,'%Y-%m') 
)
SELECT delivery_person_id, month, previous_performance, current_performance,
          current_performance - previous_performance AS improvement
FROM performance_change
WHERE previous_performance IS NOT NULL
ORDER BY improvement DESC
LIMIT 1;

-- Q3.Which cities have the highest and lowest average delivery time, 
-- and how many orders does each city handle?
(SELECT city , COUNT(*) AS total_orders,
       AVG(time_taken_min) AS avg_delivery_time
FROM zomato
GROUP BY city
ORDER BY avg_delivery_time DESC
LIMIT 1)
UNION ALL
(SELECT city , COUNT(*) AS total_orders,
       AVG(time_taken_min) AS avg_delivery_time
FROM zomato
GROUP BY city
ORDER BY avg_delivery_time ASC
LIMIT 1);

-- Q4. What percentage of orders are delayed (delivery time > 45 minutes) in each city?
SELECT city,
       ROUND(SUM(CASE WHEN time_taken_min > 45 THEN 1 END * 100.0) / 
       COUNT(*),2) AS delayed_percentage
FROM zomato
GROUP BY city;

-- Q5. Which delivery persons have the best delivery performance, 
-- considering only those who have completed at least 50 orders?
SELECT delivery_person_id,
       COUNT(*) AS total_orders, 
       ROUND(AVG(delivery_person_rating),2) AS delivery_person_performance
FROM zomato
GROUP BY delivery_person_id
HAVING COUNT(*) >= 50
ORDER BY delivery_person_performance DESC
LIMIT 1;

-- Q6.Which combination of road traffic density and weather 
-- condition results in the longest average delivery time?
SELECT
    road_traffic_density,
    weather_conditions,
    AVG(time_taken_min) AS avg_delivery_time
FROM zomato
GROUP BY road_traffic_density, weather_conditions
ORDER BY avg_delivery_time DESC
LIMIT 1;
-- Q7. How does delivery performance change month-over-month, 
-- and which month shows the biggest increase or decrease in average delivery time?
WITH previous_time AS
(SELECT DATE_FORMAT(order_date,'%Y-%m') AS month,
       AVG(delivery_person_rating) AS delivery_person_performance,
       AVG(time_taken_min) AS current_avg_delivery_time
FROM zomato
GROUP BY DATE_FORMAT(order_date,'%Y-%m')
),
 time_diff AS
(SELECT month,delivery_person_performance,
       current_avg_delivery_time,
       LAG(current_avg_delivery_time)OVER(ORDER BY month) AS previous_delivery_time
FROM previous_time)
SELECT month,delivery_person_performance,
       previous_delivery_time,
       current_avg_delivery_time,
       (current_avg_delivery_time - previous_delivery_time) AS diff_delivery_time
FROM time_diff
WHERE previous_delivery_time IS NOT NULL; 

-- Q8. Which delivery persons perform better than the average 
-- delivery time of their respective city?
WITH person_avg AS
(SELECT delivery_person_id,
       city,
       AVG(time_taken_min) AS avg_delivery_time
FROM zomato
GROUP BY delivery_person_id,
         city ),
city_avg AS        
(SELECT city,
       AVG(time_taken_min) AS city_avg_delivery_time
FROM zomato
GROUP BY city
)
SELECT p.delivery_person_id,
       p.city,
       p.avg_delivery_time,
       c.city_avg_delivery_time
FROM person_avg p
JOIN city_avg c
ON c.city = p.city
WHERE p.avg_delivery_time < c.city_avg_delivery_time
ORDER BY p.city, p.avg_delivery_time;

-- Q9. Which vehicle type and vehicle condition combination 
-- provides the best delivery performance while handling at least 100 orders?
SELECT
    type_of_vehicle,
    vehicle_condition,
    COUNT(*) AS total_orders,
    ROUND(AVG(time_taken_min), 2) AS delivery_time
FROM zomato
GROUP BY type_of_vehicle, vehicle_condition
HAVING COUNT(*) >= 100
ORDER BY delivery_time ASC
LIMIT 1;