CREATE TABLE IF NOT EXISTS listing (
    id SERIAL PRIMARY KEY,
    product_id INTEGER,
    seller_id INTEGER,
    location VARCHAR(100),
    price NUMERIC(8, 2),
    quantity SMALLINT
);

TRUNCATE TABLE listing;

INSERT INTO listing (product_id, seller_id, location, price, quantity) VALUES
  (9, 1, 'Mumbai', 43990.00, 1184), (9, 11, 'Patna', 50000.00, 103), (9, 21, 'Delhi', 74690.00, 25),
  (9, 238, 'Bangalore', 49990.00, 1033), (9, 77, 'Mumbai', 52190.00, 840), (9, 32, 'Chennai', 47890.00, 4500),
  (9, 91, 'Mumbai', 44990.00, 384), (9, 56, 'Kolkatta', 55990.00, 691), (9, 74, 'Indore', 43990.00, 1184);

INSERT INTO listing (product_id, seller_id, location, price, quantity) VALUES
  (10, 1, 'Mumbai', 43990.00, 1184), (10, 11, 'Patna', 50000.00, 103), (10, 21, 'Delhi', 74690.00, 25),
  (10, 238, 'Bangalore', 49990.00, 1033), (10, 77, 'Mumbai', 52190.00, 840), (10, 32, 'Chennai', 47890.00, 4500),
  (10, 91, 'Mumbai', 44990.00, 384), (10, 56, 'Kolkatta', 55990.00, 691), (10, 74, 'Indore', 43990.00, 1184);

INSERT INTO listing (product_id, seller_id, location, price, quantity) VALUES
  (11, 1, 'Mumbai', 43990.00, 1184), (11, 11, 'Patna', 50000.00, 103), (11, 21, 'Delhi', 74690.00, 25),
  (11, 238, 'Bangalore', 49990.00, 1033), (11, 77, 'Mumbai', 52190.00, 840), (11, 32, 'Chennai', 47890.00, 4500),
  (11, 91, 'Mumbai', 44990.00, 384), (11, 56, 'Kolkatta', 55990.00, 691), (11, 74, 'Indore', 43990.00, 1184);

INSERT INTO listing (product_id, seller_id, location, price, quantity) VALUES
  (12,  1, 'Mumbai', 33990.00, 1184), (12,  11, 'Patna', 40000.00, 103), (12,  21, 'Delhi', 64690.00, 25),
  (12,  238, 'Bangalore', 39990.00, 1033), (12,  77, 'Mumbai', 32190.00, 840), (12,  32, 'Chennai', 37890.00, 4500),
  (12,  91, 'Mumbai', 24990.00, 384), (12,  56, 'Kolkatta', 25990.00, 691), (12,  74, 'Indore', 33990.00, 1184);

INSERT INTO listing (product_id, seller_id, location, price, quantity) VALUES
  (13, 1, 'Mumbai', 33990.00, 1184), (13, 11, 'Patna', 30000.00, 103), (13, 21, 'Delhi', 24690.00, 25),
  (13, 238, 'Bangalore', 39990.00, 1033), (13, 77, 'Mumbai', 32190.00, 840), (13, 32, 'Chennai', 37890.00, 4500),
  (13, 91, 'Mumbai', 34990.00, 384), (13, 56, 'Kolkatta', 35990.00, 691), (13, 74, 'Indore', 23990.00, 1184);

INSERT INTO listing (product_id, seller_id, location, price, quantity) VALUES
  (14, 1, 'Mumbai', 33990.00, 1184), (14, 11, 'Patna', 30000.00, 103), (14, 21, 'Delhi', 24690.00, 25),
  (14, 238, 'Bangalore', 39990.00, 1033), (14, 77, 'Mumbai', 32190.00, 840), (14, 32, 'Chennai', 37890.00, 4500),
  (14, 91, 'Mumbai', 34990.00, 384), (14, 56, 'Kolkatta', 35990.00, 691), (14, 74, 'Indore', 23990.00, 1184);

INSERT INTO listing (product_id, seller_id, location, price, quantity) VALUES
  (15, 1, 'Mumbai', 33990.00, 1184), (15, 11, 'Patna', 30000.00, 103), (15, 21, 'Delhi', 24690.00, 25),
  (15, 238, 'Bangalore', 39990.00, 1033), (15, 77, 'Mumbai', 32190.00, 840), (15, 32, 'Chennai', 37890.00, 4500),
  (15, 91, 'Mumbai', 34990.00, 384), (15, 56, 'Kolkatta', 35990.00, 691), (15, 74, 'Indore', 23990.00, 1184);

INSERT INTO listing (product_id, seller_id, location, price, quantity) VALUES
  (16, 1, 'Mumbai', 33990.00, 1184), (16, 11, 'Patna', 30000.00, 103), (16, 21, 'Delhi', 24690.00, 25),
  (16, 238, 'Bangalore', 39990.00, 1033), (16, 77, 'Mumbai', 32190.00, 840), (16, 32, 'Chennai', 37890.00, 4500),
  (16, 91, 'Mumbai', 34990.00, 384), (16, 56, 'Kolkatta', 35990.00, 691), (16, 74, 'Indore', 23990.00, 1184);

INSERT INTO listing (product_id, seller_id, location, price, quantity) VALUES
  (17, 1, 'Mumbai', 33990.00, 1184), (17, 11, 'Patna', 30000.00, 103), (17, 21, 'Delhi', 24690.00, 25),
  (17, 238, 'Bangalore', 39990.00, 1033), (17, 77, 'Mumbai', 32190.00, 840), (17, 32, 'Chennai', 37890.00, 4500),
  (17, 91, 'Mumbai', 34990.00, 384), (17, 56, 'Kolkatta', 35990.00, 691), (17, 74, 'Indore', 23990.00, 1184);

INSERT INTO listing (product_id, seller_id, location, price, quantity) VALUES
  (18, 1, 'Mumbai', 33990.00, 1184), (18, 11, 'Patna', 30000.00, 103), (18, 21, 'Delhi', 24690.00, 25),
  (18, 238, 'Bangalore', 39990.00, 1033), (18, 77, 'Mumbai', 32190.00, 840), (18, 32, 'Chennai', 37890.00, 4500),
  (18, 91, 'Mumbai', 34990.00, 384), (18, 56, 'Kolkatta', 35990.00, 691), (18, 74, 'Indore', 23990.00, 1184);


