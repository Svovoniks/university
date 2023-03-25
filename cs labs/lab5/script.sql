CREATE DATABASE service_db;

\c service_db

CREATE SCHEMA service;

CREATE TABLE service.users (id SERIAL NOT NULL, full_name VARCHAR NOT NULL, login VARCHAR NOT NULL, password VARCHAR NOT NULL);

INSERT INTO service.users (full_name, login, password) VALUES 
('full_user', 'user', 'password'),
('full_user0', 'user0', 'password0'),
('full_user1', 'user1', 'password1'),
('full_user2', 'user2', 'password2'),
('full_user3', 'user3', 'password3'),
('full_user4', 'user4', 'password4'),
('full_user5', 'user5', 'password5'),
('full_user6', 'user6', 'password6'),
('full_user7', 'user7', 'password7'),
('full_user8', 'user8', 'password8');

SELECT * FROM service.users;
