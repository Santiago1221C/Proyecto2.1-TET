-- ==========================================
-- Script de inicialización de MySQL
-- ==========================================

-- Crear usuario (si no existe)
CREATE USER IF NOT EXISTS 'bookstore'@'%' IDENTIFIED BY 'bookstore123';
CREATE USER IF NOT EXISTS 'bookstore'@'localhost' IDENTIFIED BY 'bookstore123';

-- Crear bases de datos necesarias
CREATE DATABASE IF NOT EXISTS catalogdb;
CREATE DATABASE IF NOT EXISTS cartdb;
CREATE DATABASE IF NOT EXISTS orderdb;
CREATE DATABASE IF NOT EXISTS userdb;

-- Conceder privilegios
GRANT ALL PRIVILEGES ON catalogdb.* TO 'bookstore'@'%';
GRANT ALL PRIVILEGES ON cartdb.* TO 'bookstore'@'%';
GRANT ALL PRIVILEGES ON orderdb.* TO 'bookstore'@'%';
GRANT ALL PRIVILEGES ON userdb.* TO 'bookstore'@'%';

GRANT ALL PRIVILEGES ON catalogdb.* TO 'bookstore'@'localhost';
GRANT ALL PRIVILEGES ON cartdb.* TO 'bookstore'@'localhost';
GRANT ALL PRIVILEGES ON orderdb.* TO 'bookstore'@'localhost';
GRANT ALL PRIVILEGES ON userdb.* TO 'bookstore'@'localhost';

FLUSH PRIVILEGES;