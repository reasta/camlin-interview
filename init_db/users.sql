CREATE DATABASE IF NOT EXISTS camlin_db;

USE camlin_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
  
    username VARCHAR(100),
    full_name VARCHAR(100),
    email VARCHAR(100),
    hashed_password VARCHAR(100),
    eur DECIMAL(20,2),
    usd DECIMAL(20,2),
    jpy DECIMAL(20,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, full_name, email, hashed_password, eur, usd, jpy) 
VALUES
('dristic', 'Dusan Ristc', 'dristic@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 100, 20, 8000), /*pass: secret*/
('dmirkovic', 'Darko Mirkovic', 'dmirkovic@example.com', '$2b$12$kyNKhLbvM6Sm9WUDWBYcKOHcJtK5cYawHV2KusgTeAwzfdM.BgsxG', 100, 20, 8000), /*pass: darkopass*/
('mlesniewski', 'Michal Lesniewski', 'mlesniewski@example.com', '$2b$12$XMrjwy5y2Yji.BQ/tcQtcOAoIGVdu2iqR5cJNhOIhEoQrS50SkGmW', 100, 20, 8000); /*pass: michalpass*/
