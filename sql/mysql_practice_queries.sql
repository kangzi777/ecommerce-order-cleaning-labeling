-- 电商订单数据查询练习
-- 数据表：orders
-- 说明：本文件用于记录订单数据导入 MySQL 后的基础查询、数据核验与统计分析语句。
-- 注意：本文件不包含数据库账号、密码、本机路径或个人隐私信息。

-- 1. 查看订单总量
SELECT COUNT(*) AS total_orders
FROM orders;

-- 2. 查看前10条订单
SELECT *
FROM orders
LIMIT 10;

-- 3. 查看常用字段
SELECT
    order_id,
    order_date,
    customer_id,
    province,
    city,
    category,
    product_name,
    quantity,
    unit_price,
    order_status
FROM orders
LIMIT 20;

-- 4. 查询浙江省订单
SELECT *
FROM orders
WHERE province = '浙江';

-- 5. 查询已完成订单
SELECT *
FROM orders
WHERE order_status = '已完成';

-- 6. 查询单价较高的订单
SELECT *
FROM orders
WHERE unit_price > 500
ORDER BY unit_price DESC;

-- 7. 查询数量为空或小于等于0的记录
SELECT *
FROM orders
WHERE quantity IS NULL
   OR quantity <= 0;

-- 8. 查询客户ID缺失记录
SELECT *
FROM orders
WHERE customer_id IS NULL
   OR customer_id = '';

-- 9. 查询省份或城市缺失记录
SELECT *
FROM orders
WHERE province IS NULL
   OR province = ''
   OR city IS NULL
   OR city = '';

-- 10. 查询重复订单ID
SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 11. 按商品类别统计订单数
SELECT
    category,
    COUNT(*) AS order_count
FROM orders
GROUP BY category
ORDER BY order_count DESC;

-- 12. 按省份统计订单数
SELECT
    province,
    COUNT(*) AS order_count
FROM orders
GROUP BY province
ORDER BY order_count DESC;

-- 13. 按城市统计订单数
SELECT
    city,
    COUNT(*) AS order_count
FROM orders
GROUP BY city
ORDER BY order_count DESC;

-- 14. 按订单状态统计订单数
SELECT
    order_status,
    COUNT(*) AS order_count
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;

-- 15. 计算每条订单的实际金额
SELECT
    order_id,
    product_name,
    quantity,
    unit_price,
    discount,
    quantity * unit_price * (1 - IFNULL(discount, 0)) AS actual_amount
FROM orders;

-- 16. 按商品类别统计销售额
SELECT
    category,
    SUM(quantity * unit_price * (1 - IFNULL(discount, 0))) AS total_amount
FROM orders
GROUP BY category
ORDER BY total_amount DESC;

-- 17. 按省份统计销售额
SELECT
    province,
    SUM(quantity * unit_price * (1 - IFNULL(discount, 0))) AS total_amount
FROM orders
GROUP BY province
ORDER BY total_amount DESC;

-- 18. 查询单价为空的记录
SELECT *
FROM orders
WHERE unit_price IS NULL;

-- 19. 查询折扣异常记录
SELECT *
FROM orders
WHERE discount IS NULL
   OR discount < 0
   OR discount > 1;

-- 20. 按月份统计订单数
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS order_month,
    COUNT(*) AS order_count
FROM orders
WHERE order_date IS NOT NULL
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY order_month;

-- 21. 按月份统计销售额
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS order_month,
    SUM(quantity * unit_price * (1 - IFNULL(discount, 0))) AS total_amount
FROM orders
WHERE order_date IS NOT NULL
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY order_month;

-- 22. 按商品类别统计平均单价
SELECT
    category,
    AVG(unit_price) AS avg_unit_price
FROM orders
WHERE unit_price IS NOT NULL
GROUP BY category
ORDER BY avg_unit_price DESC;

-- 23. 查询疑似高金额订单
SELECT
    order_id,
    customer_id,
    product_name,
    quantity,
    unit_price,
    discount,
    quantity * unit_price * (1 - IFNULL(discount, 0)) AS actual_amount
FROM orders
WHERE quantity * unit_price * (1 - IFNULL(discount, 0)) > 1000
ORDER BY actual_amount DESC;

-- 24. 按支付方式统计订单数
SELECT
    payment_method,
    COUNT(*) AS order_count
FROM orders
GROUP BY payment_method
ORDER BY order_count DESC;

-- 25. 按商品类别和订单状态交叉统计
SELECT
    category,
    order_status,
    COUNT(*) AS order_count
FROM orders
GROUP BY category, order_status
ORDER BY category, order_count DESC;
