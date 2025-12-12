-----------------------------------------------------
-- ELIMINAR TABLAS EXISTENTES (ORDEN CORRECTO)
-----------------------------------------------------
DROP TABLE IF EXISTS access_control CASCADE;
DROP TABLE IF EXISTS payment CASCADE;
DROP TABLE IF EXISTS registration CASCADE;
DROP TABLE IF EXISTS notification CASCADE;
DROP TABLE IF EXISTS report CASCADE;
DROP TABLE IF EXISTS event CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS role CASCADE;

-----------------------------------------------------
-- TABLA ROLE
-----------------------------------------------------
CREATE TABLE role (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL,
    permissions TEXT
);

-----------------------------------------------------
-- TABLA USERS
-----------------------------------------------------
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role_id INTEGER REFERENCES role(role_id)
);

-----------------------------------------------------
-- TABLA EVENT
-----------------------------------------------------
CREATE TABLE event (
    event_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    location VARCHAR(200),
    category VARCHAR(200),
    capacity INTEGER,
    status VARCHAR(50)
);

-----------------------------------------------------
-- TABLA REPORT
-----------------------------------------------------
CREATE TABLE report (
    report_id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES event(event_id),
    total_registrations INTEGER,
    confirmed_attendance INTEGER,
    total_payments DECIMAL(12,2),
    generated_at TIMESTAMP DEFAULT NOW()
);

-----------------------------------------------------
-- TABLA NOTIFICATION
-----------------------------------------------------
CREATE TABLE notification (
    notification_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    event_id INTEGER REFERENCES event(event_id),
    message TEXT,
    type VARCHAR(50),
    sent_at TIMESTAMP DEFAULT NOW()
);

-----------------------------------------------------
-- TABLA REGISTRATION
-----------------------------------------------------
CREATE TABLE registration (
    registration_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    event_id INTEGER REFERENCES event(event_id),
    registration_date DATE DEFAULT NOW(),
    status VARCHAR(50),
    qr_code TEXT
);

-----------------------------------------------------
-- TABLA PAYMENT
-----------------------------------------------------
CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    registration_id INTEGER REFERENCES registration(registration_id),
    amount DECIMAL(12,2),
    status VARCHAR(50),
    transaction_date DATE DEFAULT NOW(),
    payment_reference TEXT
);

-----------------------------------------------------
-- TABLA ACCESS CONTROL
-----------------------------------------------------
CREATE TABLE access_control (
    access_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    login_time TIMESTAMP DEFAULT NOW(),
    logout_time TIMESTAMP,
    token TEXT
);

SELECT * FROM users;
SELECT * FROM users WHERE email LIKE '%unal.edu.co'; -- Validar solo @unal

INSERT INTO event (title, description, date, location, category, capacity, status)
VALUES (
    'Taller de Introducción a QUERCUS',
    'Sesión para presentar la plataforma de eventos de la comunidad UNAL.',
    '2025-12-15',
    'Auditorio Principal',
    'Académico',
    100,
    'activo'
); -- Probando creación manual de evento

INSERT INTO event (title, description, date, location, category, capacity, status)
VALUES (
    'Taller de Introducción a IA',
    'Sesión para presentar la plataforma IA elaborada en Ing Soft II.',
    '2025-12-12',
    'Auditorio León de Fr',
    'Académico',
    100,
    'activo'
); -- Probando creación manual de evento

SELECT * FROM event;
DELETE FROM event
WHERE event_id = 1;
SELECT * FROM registration; -- Verificar registros
