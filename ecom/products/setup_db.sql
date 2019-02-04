CREATE USER ecom_user WITH CREATEDB PASSWORD 'test_password';
\c postgres ecom_user

CREATE DATABASE ecom;
\c ecom

CREATE TABLE IF NOT EXISTS product (
    id SERIAL PRIMARY KEY,
    model_number VARCHAR(100),
    title VARCHAR(250),
    description TEXT,
    brand_name VARCHAR(100),
    variant TEXT,
    details TEXT
);

TRUNCATE TABLE product;

INSERT INTO product (model_number, title, description, brand_name, variant, details) VALUES (
  'SM-N950F',
  'Samsung Galaxy Note 8',
  'Camera: 12+12 MP Dual rear Camera with Autofocus, 2x Optical zoom | 8 MP front camera with Image recording, Touch focus and Face smile detection',
  'Samsung',
  '{"color": "Midnight Black", "memory": "6GB", "storage": "64GB"}',
  '{"OS": "Android", "Weight": "195 g", "Phone Talk Time": "22 Hours"}');

INSERT INTO product (model_number, title, description, brand_name, variant, details) VALUES (
  'SM-N950FZVDINS',
  'Samsung Galaxy Note 8',
  'Camera: 12+12 MP Dual rear Camera with Autofocus, 2x Optical zoom | 8 MP front camera with Image recording, Touch focus and Face smile detection',
  'Samsung',
  '{"color": "Orchid Grey", "memory": "6GB", "storage": "64GB"}',
  '{"OS": "Android", "Weight": "195 g", "Phone Talk Time": "22 Hours"}');

INSERT INTO product (model_number, title, description, brand_name, variant, details) VALUES (
  'SM-N950F',
  'Samsung Galaxy Note 8',
  'Camera: 12+12 MP Dual rear Camera with Autofocus, 2x Optical zoom | 8 MP front camera with Image recording, Touch focus and Face smile detection',
  'Samsung',
  '{"color": "Maple Gold", "memory": "6GB", "storage": "64GB"}',
  '{"OS": "Android", "Weight": "195 g", "Phone Talk Time": "22 Hours"}');

INSERT INTO product (model_number, title, description, brand_name, variant, details) VALUES (
  'SM-A920FZBDINS',
  'Samsung Galaxy A9',
  '24MP+ 5MP + 10MP +8MP rear camera with auto focus, rear LED flash, digital zoom up to 10x, optical zoom up to 2x and 24MP front facing camera',
  'Samsung',
  '{"color": "Lemonade Blue", "memory": "6GB", "storage": "128GB"}',
  '{"OS": "Android", "Weight": "191 g", "Product Dimensions": "16.2 x 0.8 x 7.7 cm"}');

INSERT INTO product (model_number, title, description, brand_name, variant, details) VALUES (
  'A6010',
  'OnePlus 6T',
  'Camera: 16+20 MP Dual rear camera with Optical Image Stabilization, Super slow motion, Nightscape and Studio Lighting | 16 MP front camera',
  'OnePlus',
  '{"color": "Mirror Black", "memory": "8GB", "storage": "128GB"}',
  '{"OS": "Android", "Weight": "186 g", "Display technology": "AMOLED"}');

INSERT INTO product (model_number, title, description, brand_name, variant, details) VALUES (
  'A6010',
  'OnePlus 6T',
  'Camera: 16+20 MP Dual rear camera with Optical Image Stabilization, Super slow motion, Nightscape and Studio Lighting | 16 MP front camera',
  'OnePlus',
  '{"color": "Mirror Black", "memory": "6GB", "storage": "256GB"}',
  '{"OS": "Android", "Weight": "186 g", "Display technology": "AMOLED"}');

INSERT INTO product (model_number, title, description, brand_name, variant, details) VALUES (
  'A6010',
  'OnePlus 6T',
  'Camera: 16+20 MP Dual rear camera with Optical Image Stabilization, Super slow motion, Nightscape and Studio Lighting | 16 MP front camera',
  'OnePlus',
  '{"color": "Mirror Black", "memory": "10GB", "storage": "256GB"}',
  '{"OS": "Android", "Weight": "186 g", "Display technology": "AMOLED"}');

INSERT INTO product (model_number, title, description, brand_name, variant, details) VALUES (
  'Pixel3_XL_64',
  'Google Pixel 3 XL',
  '12.2MP rear camera | 8MP+8MP dual front camera',
  'Google',
  '{"color": "Just Black", "memory": "4GB", "storage": "64GB"}',
  '{"OS": "Android", "Weight": "186 g", "Product Dimensions": "15.8 x 0.8 x 7.6 cm"}');

INSERT INTO product (model_number, title, description, brand_name, variant, details) VALUES (
  'Pixel 3_ 64',
  'Google Pixel 3',
  '12.2MP rear camera | 8MP+8MP dual front camera',
  'Google',
  '{"color": "Just Black", "memory": "4GB", "storage": "64GB"}',
  '{"OS": "Android", "Weight": "145 g", "Product Dimensions": "15.8 x 0.8 x 7.6 cm"}');

INSERT INTO product (model_number, title, description, brand_name, variant, details) VALUES (
  'CLT-AL00',
  'Huawei P20 Pro',
  'Camera: 40+20+8 MP Triple Rear camera with 3D Portrait lighting, 5x Hybrid zoom, AI Image stabilization and 960 fps Super slow video mode | 24 MP front camera with 3D Portrait lighting',
  'Huawei',
  '{"color": "Blue", "memory": "6GB", "storage": "128GB"}',
  '{"OS": "Android", "Weight": "181 g", "Product Dimensions": "15.5 x 0.8 x 7.4 cm"}');

