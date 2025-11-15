-- ==========================================
-- Script de inicialización de MySQL
-- Bookstore Microservices
-- ==========================================

-- Crear usuario (si no existe)
CREATE USER IF NOT EXISTS 'bookstore'@'%' IDENTIFIED BY 'bookstore123';
CREATE USER IF NOT EXISTS 'bookstore'@'localhost' IDENTIFIED BY 'bookstore123';

-- ==========================================
-- BASES DE DATOS
-- ==========================================

-- Microservicios Java (Spring Boot)
CREATE DATABASE IF NOT EXISTS catalogdb;
CREATE DATABASE IF NOT EXISTS cartdb;
CREATE DATABASE IF NOT EXISTS orderdb;
CREATE DATABASE IF NOT EXISTS userdb;

-- Microservicios Python (Flask/FastAPI)
CREATE DATABASE IF NOT EXISTS review_db;
CREATE DATABASE IF NOT EXISTS payment_db;

-- ==========================================
-- PRIVILEGIOS - Remote connections (%)
-- ==========================================
GRANT ALL PRIVILEGES ON catalogdb.* TO 'bookstore'@'%';
GRANT ALL PRIVILEGES ON cartdb.* TO 'bookstore'@'%';
GRANT ALL PRIVILEGES ON orderdb.* TO 'bookstore'@'%';
GRANT ALL PRIVILEGES ON userdb.* TO 'bookstore'@'%';
GRANT ALL PRIVILEGES ON review_db.* TO 'bookstore'@'%';
GRANT ALL PRIVILEGES ON payment_db.* TO 'bookstore'@'%';

-- ==========================================
-- PRIVILEGIOS - Localhost connections
-- ==========================================
GRANT ALL PRIVILEGES ON catalogdb.* TO 'bookstore'@'localhost';
GRANT ALL PRIVILEGES ON cartdb.* TO 'bookstore'@'localhost';
GRANT ALL PRIVILEGES ON orderdb.* TO 'bookstore'@'localhost';
GRANT ALL PRIVILEGES ON userdb.* TO 'bookstore'@'localhost';
GRANT ALL PRIVILEGES ON review_db.* TO 'bookstore'@'localhost';
GRANT ALL PRIVILEGES ON payment_db.* TO 'bookstore'@'localhost';

FLUSH PRIVILEGES;

-- ==========================================
-- Verificación
-- ==========================================
SELECT 'Bases de datos creadas exitosamente' AS Status;
SHOW DATABASES;