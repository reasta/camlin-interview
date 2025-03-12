CREATE DATABASE IF NOT EXISTS camlin_db;

USE camlin_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
  
    username VARCHAR(100),
    full_name VARCHAR(100),
    email VARCHAR(100),
    hashed_password VARCHAR(100),
    eur DECIMAL,
    usd DECIMAL,
    jpy DECIMAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, full_name, email, hashed_password, eur, usd, jpy) 
VALUES ('dristic', 'Dusan Ristc', 'dristic@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 100, 20, 8000);
