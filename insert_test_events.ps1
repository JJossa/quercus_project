# Script para insertar eventos de prueba en la base de datos quercus_db
# Los eventos estan disenados para probar diferentes roles: estudiante, organizador, admin
# Ejecutar desde PowerShell en Windows

# Configurar credenciales
$pgPassword = "password"
$pgUser = "postgres"
$dbName = "quercus_db"

# Archivo SQL con los eventos de prueba
$sqlScript = @"
-- Insertar eventos de prueba con diferentes organizadores y ubicaciones
-- Asumiendo que los usuarios existen: user_id 1 (admin), 2 (organizador), 3 (estudiante)

-- EVENTO 1: Charla en Bogota (Organizador: user_id 2)
INSERT INTO event (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Charla: Introduccion a Python',
  'Una charla introductoria sobre los fundamentos de Python. Perfecta para principiantes.',
  '2025-12-20',
  '10:00',
  'Bogota',
  'Charla',
  50,
  2,
  'activo'
);

-- EVENTO 2: Conferencia en Medellin (Organizador: user_id 2)
INSERT INTO event (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Conferencia: Tendencias en IA 2025',
  'Descubre las ultimas tendencias en inteligencia artificial y machine learning.',
  '2025-12-22',
  '14:00',
  'Medellin',
  'Conferencia',
  100,
  2,
  'activo'
);

-- EVENTO 3: Taller en Palmira (Organizador: user_id 2)
INSERT INTO event (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Taller: Git y Control de Versiones',
  'Aprende a usar Git desde lo basico. Incluye practicas hands-on.',
  '2025-12-25',
  '09:00',
  'Palmira',
  'Taller',
  30,
  2,
  'activo'
);

-- EVENTO 4: Seminario en Manizales (Organizador: user_id 2)
INSERT INTO event (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Seminario: Seguridad en Aplicaciones Web',
  'Conoce las mejores practicas de seguridad para desarrollo web.',
  '2025-12-28',
  '15:30',
  'Manizales',
  'Seminario',
  40,
  2,
  'activo'
);

-- EVENTO 5: Mesa redonda en Bogota (Organizador: user_id 2)
INSERT INTO event (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Mesa Redonda: Carrera en Tech',
  'Panel de expertos hablando sobre oportunidades laborales en tecnologia.',
  '2025-12-30',
  '16:00',
  'Bogota',
  'Mesa redonda',
  60,
  2,
  'activo'
);

-- EVENTO 6: Charla en Medellin (Organizador: user_id 2)
INSERT INTO event (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Charla: Testing Automatizado',
  'Mejora la calidad de tu codigo con testing automatizado.',
  '2025-12-31',
  '11:00',
  'Medellin',
  'Charla',
  45,
  2,
  'activo'
);

-- EVENTO 7: Taller en Manizales (Organizador: user_id 2)
INSERT INTO event (title, description, date, time, location, category, capacity, organizer_id, status)
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
INSERT INTO event (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Conferencia: Cloud Computing',
  'Explora las soluciones cloud mas populares: AWS, Azure, GCP.',
  '2026-01-15',
  '13:00',
  'Palmira',
  'Conferencia',
  80,
  2,
  'activo'
);

-- EVENTO 9: Seminario en Bogota (Organizador: user_id 2)
INSERT INTO event (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Seminario: Emprendimiento Tech',
  'De la idea al MVP: como lanzar tu startup tecnologica.',
  '2026-01-20',
  '14:00',
  'Bogota',
  'Seminario',
  50,
  2,
  'activo'
);

-- EVENTO 10: Mesa redonda en Manizales (Organizador: user_id 2)
INSERT INTO event (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Mesa Redonda: Etica en IA',
  'Discusion sobre consideraciones eticas en desarrollo de IA.',
  '2026-01-25',
  '15:00',
  'Manizales',
  'Mesa redonda',
  55,
  2,
  'activo'
);

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
FROM event
WHERE title LIKE 'PRUEBA%'
ORDER BY date, time;

SELECT COUNT(*) as total_eventos_prueba FROM event WHERE title LIKE 'PRUEBA%';
"@

# Guardar el script SQL en un archivo temporal
$sqlFile = [System.IO.Path]::GetTempFileName()
$sqlFile = $sqlFile -replace '\.tmp$', '.sql'
Set-Content -Path $sqlFile -Value $sqlScript

try {
    Write-Host "Insertando eventos de prueba en la base de datos..." -ForegroundColor Cyan
    
    # Ejecutar el script SQL con psql
    & psql -U $pgUser -d $dbName -f $sqlFile
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Eventos de prueba insertados exitosamente." -ForegroundColor Green
        Write-Host ""
        Write-Host "Resumen de eventos insertados:" -ForegroundColor Yellow
        & psql -U $pgUser -d $dbName -c "SELECT COUNT(*) as total_eventos_prueba FROM event WHERE title LIKE 'PRUEBA%';"
    } else {
        Write-Host "Error al insertar eventos de prueba." -ForegroundColor Red
    }
}
finally {
    # Limpiar el archivo temporal
    if (Test-Path $sqlFile) {
        Remove-Item $sqlFile -Force
    }
}

Write-Host ""
Write-Host "Eventos agregados:" -ForegroundColor Yellow
Write-Host "  1. Charla: Introduccion a Python (Bogota, 2025-12-20)" -ForegroundColor White
Write-Host "  2. Conferencia: Tendencias en IA (Medellin, 2025-12-22)" -ForegroundColor White
Write-Host "  3. Taller: Git y Control de Versiones (Palmira, 2025-12-25)" -ForegroundColor White
Write-Host "  4. Seminario: Seguridad en Aplicaciones Web (Manizales, 2025-12-28)" -ForegroundColor White
Write-Host "  5. Mesa Redonda: Carrera en Tech (Bogota, 2025-12-30)" -ForegroundColor White
Write-Host "  6. Charla: Testing Automatizado (Medellin, 2025-12-31)" -ForegroundColor White
Write-Host "  7. Taller: React Fundamentals (Manizales, 2026-01-10)" -ForegroundColor White
Write-Host "  8. Conferencia: Cloud Computing (Palmira, 2026-01-15)" -ForegroundColor White
Write-Host "  9. Seminario: Emprendimiento Tech (Bogota, 2026-01-20)" -ForegroundColor White
Write-Host "  10. Mesa Redonda: Etica en IA (Manizales, 2026-01-25)" -ForegroundColor White
Write-Host ""
Write-Host "Sedes disponibles: Bogota, Medellin, Palmira, Manizales" -ForegroundColor Green
Write-Host "Tipos de eventos: Charla, Conferencia, Taller, Seminario, Mesa redonda" -ForegroundColor Green
Write-Host ""
Write-Host "Tip: Los eventos estan marcados con PRUEBA- para identificarlos facilmente." -ForegroundColor Cyan
