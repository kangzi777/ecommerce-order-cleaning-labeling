CREATE DATABASE IF NOT EXISTS ai_data_practice;
USE ai_data_practice;

DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    order_id VARCHAR(50),
    order_date DATE,
    customer_id VARCHAR(50),
    province VARCHAR(50),
    city VARCHAR(50),
    category VARCHAR(50),
    product_name VARCHAR(100),
    quantity INT,
    unit_price DECIMAL(10,2),
    discount DECIMAL(6,4),
    payment_method VARCHAR(50),
    order_status VARCHAR(50),
    customer_review TEXT
);
