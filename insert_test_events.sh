#!/bin/bash

# Script para insertar eventos de prueba en la base de datos quercus_db
# Los eventos están diseñados para probar diferentes roles: estudiante, organizador, admin

PGPASSWORD="password" psql -U postgres -d quercus_db << EOF

-- Limitar datos previos (opcional: comentar para conservar eventos existentes)
-- DELETE FROM events WHERE title LIKE 'PRUEBA%';

-- Insertar eventos de prueba con diferentes organizadores y ubicaciones
-- Asumiendo que los usuarios existen: user_id 1 (admin), 2 (organizador), 3 (estudiante)

-- EVENTO 1: Charla en Bogotá (Organizador: user_id 2)
INSERT INTO events (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Charla: Introducción a Python',
  'Una charla introductoria sobre los fundamentos de Python. Perfecta para principiantes.',
  '2025-12-20',
  '10:00',
  'Bogotá',
  'Charla',
  50,
  2,
  'activo'
);

-- EVENTO 2: Conferencia en Medellín (Organizador: user_id 2)
INSERT INTO events (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Conferencia: Tendencias en IA 2025',
  'Descubre las últimas tendencias en inteligencia artificial y machine learning.',
  '2025-12-22',
  '14:00',
  'Medellín',
  'Conferencia',
  100,
  2,
  'activo'
);

-- EVENTO 3: Taller en Palmira (Organizador: user_id 2)
INSERT INTO events (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Taller: Git y Control de Versiones',
  'Aprende a usar Git desde lo básico. Incluye prácticas hands-on.',
  '2025-12-25',
  '09:00',
  'Palmira',
  'Taller',
  30,
  2,
  'activo'
);

-- EVENTO 4: Seminario en Manizales (Organizador: user_id 2)
INSERT INTO events (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Seminario: Seguridad en Aplicaciones Web',
  'Conoce las mejores prácticas de seguridad para desarrollo web.',
  '2025-12-28',
  '15:30',
  'Manizales',
  'Seminario',
  40,
  2,
  'activo'
);

-- EVENTO 5: Mesa redonda en Bogotá (Organizador: user_id 2)
INSERT INTO events (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Mesa Redonda: Carrera en Tech',
  'Panel de expertos hablando sobre oportunidades laborales en tecnología.',
  '2025-12-30',
  '16:00',
  'Bogotá',
  'Mesa redonda',
  60,
  2,
  'activo'
);

-- EVENTO 6: Charla en Medellín (Organizador: user_id 2)
INSERT INTO events (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Charla: Testing Automatizado',
  'Mejora la calidad de tu código con testing automatizado.',
  '2025-12-31',
  '11:00',
  'Medellín',
  'Charla',
  45,
  2,
  'activo'
);

-- EVENTO 7: Taller en Manizales (Organizador: user_id 2)
INSERT INTO events (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Taller: React Fundamentals',
  'Aprende a construir interfaces modernas con React.',
  '2026-01-10',
  '10:00',
  'Manizales',
  'Taller',
  35,
  2,
  'activo'
);

-- EVENTO 8: Conferencia en Palmira (Organizador: user_id 2)
INSERT INTO events (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Conferencia: Cloud Computing',
  'Explora las soluciones cloud más populares: AWS, Azure, GCP.',
  '2026-01-15',
  '13:00',
  'Palmira',
  'Conferencia',
  80,
  2,
  'activo'
);

-- EVENTO 9: Seminario en Bogotá (Organizador: user_id 2)
INSERT INTO events (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Seminario: Emprendimiento Tech',
  'De la idea al MVP: cómo lanzar tu startup tecnológica.',
  '2026-01-20',
  '14:00',
  'Bogotá',
  'Seminario',
  50,
  2,
  'activo'
);

-- EVENTO 10: Mesa redonda en Manizales (Organizador: user_id 2)
INSERT INTO events (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Mesa Redonda: Ética en IA',
  'Discusión sobre consideraciones éticas en desarrollo de IA.',
  '2026-01-25',
  '15:00',
  'Manizales',
  'Mesa redonda',
  55,
  2,
  'activo'
);

COMMIT;

-- Mostrar los eventos insertados
SELECT 
  event_id,
  title,
  date,
  time,
  location,
  category,
  capacity,
  organizer_id,
  status
FROM events
WHERE title LIKE 'PRUEBA%'
ORDER BY date, time;

EOF

echo "✅ Eventos de prueba insertados exitosamente."
echo ""
echo "📊 Resumen de eventos insertados:"
PGPASSWORD="password" psql -U postgres -d quercus_db -c "SELECT COUNT(*) as total_eventos_prueba FROM events WHERE title LIKE 'PRUEBA%';"
