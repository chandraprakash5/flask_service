CREATE TABLE IF NOT EXISTS payment (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    payment_mode VARCHAR(50),
    mode_details TEXT,
    amount NUMERIC(8, 2),
    status VARCHAR(20),
    error_details TEXT,
    transaction_date DATE
);

TRUNCATE TABLE payment;

