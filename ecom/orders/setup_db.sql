CREATE TABLE IF NOT EXISTS order_item (
    order_id INT NOT NULL,
    listing_id INT NOT NULL,
    quantity SMALLINT,
    unit_price NUMERIC(8, 2),
    estimated_delivery_date DATE,
    delivery_charges NUMERIC(8, 2),

    PRIMARY KEY (order_id, listing_id)
);

CREATE TABLE IF NOT EXISTS customer_order (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    order_date TIMESTAMP,
    payment_status VARCHAR(20),
    delivery_address TEXT
);

