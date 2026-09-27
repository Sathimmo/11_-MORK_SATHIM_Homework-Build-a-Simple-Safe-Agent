-- 5. Insert Users
INSERT INTO users (username, email, password_hash, role, phone) VALUES
('admin', 'admin@restaurant.com', 'Admin123', 'ADMIN', '012345678'),
('visal_dev', 'visal@gmail.com', '1234', 'CUSTOMER', '098765432'),
('srey_leak', 'sreyleak@gmail.com', '1234', 'CUSTOMER', '011223344'),
('admin_sothea', 'sothea.admin@library.com', 'hashed_pw_1', 'ADMIN', '022334455'),
('customer_sophea', 'sophea.customer@library.com', 'hashed_pw_2', 'CUSTOMER', '088776655');

-- 6. Insert Sample Library Books
INSERT INTO books (title, author, isbn, total_copies, available_copies) VALUES
('Clean Code: A Handbook of Agile Software Craftsmanship', 'Robert C. Martin', '978-0132350884', 5, 4),
('Spring Boot in Action', 'Craig Walls', '978-1617292547', 3, 3),
('PostgreSQL: Up and Running', 'Regina O. Obe', '978-1449373030', 4, 4),
('Java: The Complete Reference', 'Herbert Schildt', '978-1260440232', 2, 2),
('Introduction to Algorithms', 'Thomas H. Cormen', '978-0262033848', 3, 3);

-- 7. Insert Sample Borrowing Record
INSERT INTO borrowings (user_id, book_id, due_date, status) VALUES
(2, 1, CURRENT_TIMESTAMP + INTERVAL '14 days', 'ACTIVE');