CREATE TABLE IF NOT EXISTS review (
    id SERIAL PRIMARY KEY,
    user_id INT,
    model_number VARCHAR(100),
    rating SMALLINT,
    review_text TEXT,
    review_date DATE
);

TRUNCATE TABLE review;

INSERT INTO review (user_id, model_number, rating, review_text, review_date) VALUES
  (25, 'SM-N950F', 4, 'Good', now()),
  (35, 'SM-N950F', 3, 'Ok', now()),
  (55, 'SM-N950F', 3, 'Ok', now()),
  (125, 'SM-N950F', 5, 'Good', now()),
  (254, 'SM-N950F', 3, 'Ok', now()),
  (258, 'SM-N950F', 2, 'Bad', now()),
  (2, 'SM-N950F', 5, 'Great', now()),
  (245, 'SM-N950F', 5, 'Great', now()),
  (298, 'SM-N950F', 5, 'Great', now()),
  (1276, 'SM-N950F', 5, 'Great', now());

INSERT INTO review (user_id, model_number, rating, review_text, review_date) VALUES
  (32, 'SM-N950FZVDINS', 4, 'Good', now()),
  (352, 'SM-N950FZVDINS', 5, 'Great', now()),
  (382, 'SM-N950FZVDINS', 5, 'Great', now()),
  (1382, 'SM-N950FZVDINS', 5, 'Great', now()),
  (3210, 'SM-N950FZVDINS', 3, 'Ok', now()),
  (3325, 'SM-N950FZVDINS', 1, 'Worst', now());

INSERT INTO review (user_id, model_number, rating, review_text, review_date) VALUES
  (2473, 'SM-A920FZBDINS', 3, 'OK', now()),
  (2743, 'SM-A920FZBDINS', 2, 'Bad', now()),
  (7243, 'SM-A920FZBDINS', 2, 'Bad', now()),
  (2437, 'SM-A920FZBDINS', 2, 'Bad', now()),
  (12743, 'SM-A920FZBDINS', 1, 'Worst', now()),
  (72143, 'SM-A920FZBDINS', 1, 'Worst', now()),
  (12437, 'SM-A920FZBDINS', 5, 'Great', now()),
  (72473, 'SM-A920FZBDINS', 4, 'Good', now());

INSERT INTO review (user_id, model_number, rating, review_text, review_date) VALUES
  (1324, 'A6010', 5, 'Great', now()),
  (12, 'A6010', 4, 'Great', now()),
  (13345, 'A6010', 3, 'OK', now());

INSERT INTO review (user_id, model_number, rating, review_text, review_date) VALUES
  (9856, 'Pixel3_XL_64', 1, 'Worst', now()),
  (5985, 'Pixel3_XL_64', 1, 'Worst', now()),
  (5968, 'Pixel3_XL_64', 2, 'Bad', now()),
  (6985, 'Pixel3_XL_64', 2, 'Bad', now()),
  (986, 'Pixel3_XL_64', 2, 'Bad', now()),
  (968, 'Pixel3_XL_64', 1, 'Worst', now()),
  (698, 'Pixel3_XL_64', 2, 'Bad', now());

INSERT INTO review (user_id, model_number, rating, review_text, review_date) VALUES
  (9234, 'Pixel 3_ 64', 4, 'Good', now()),
  (2394, 'Pixel 3_ 64', 4, 'Good', now());

INSERT INTO review (user_id, model_number, rating, review_text, review_date) VALUES
  (90831, 'CLT-AL00', 5, 'Great', now()),
  (98031, 'CLT-AL00', 3, 'Ok', now()),
  (98310, 'CLT-AL00', 3, 'Ok', now()),
  (98301, 'CLT-AL00', 3, 'Ok', now()),
  (198310, 'CLT-AL00', 5, 'Great', now());

