USE ai_data_practice;

-- 1. 查看总记录数
SELECT COUNT(*) AS total_rows
FROM orders;

-- 2. 查看前10条记录
SELECT *
FROM orders
LIMIT 10;

-- 3. 按商品类别统计订单数
SELECT
    category,
    COUNT(*) AS order_count
FROM orders
GROUP BY category
ORDER BY order_count DESC;

-- 4. 按省份统计订单数
SELECT
    province,
    COUNT(*) AS order_count
FROM orders
GROUP BY province
ORDER BY order_count DESC;

-- 5. 按订单状态统计订单数
SELECT
    order_status,
    COUNT(*) AS order_count
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;

-- 6. 查询重复订单ID
SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 7. 查询客户ID缺失记录
SELECT *
FROM orders
WHERE customer_id IS NULL OR customer_id = '';

-- 8. 查询数量异常记录
SELECT *
FROM orders
WHERE quantity IS NULL OR quantity <= 0;

-- 9. 计算各类别销售额
SELECT
    category,
    ROUND(SUM(quantity * unit_price * (1 - IFNULL(discount, 0))), 2) AS total_amount
FROM orders
GROUP BY category
ORDER BY total_amount DESC;

-- 10. 查询浙江省已完成订单
SELECT *
FROM orders
WHERE province = '浙江'
  AND order_status = '已完成';
