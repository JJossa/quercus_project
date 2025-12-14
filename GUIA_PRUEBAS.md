# Guia de Prueba - Eventos de Ejemplo

Este documento explica como usar los scripts para insertar eventos de prueba en la base de datos.

## Contenido

He creado dos scripts para insertar eventos de prueba:

1. **insert_test_events.ps1** - Script PowerShell (para Windows)
2. **insert_test_events.sh** - Script Bash (para Linux/Mac)

## Eventos Insertados

Se insertan 10 eventos de prueba distribuidos en 4 sedes colombianas:

| ID | Evento | Tipo | Sede | Fecha | Organizador |
|----|----|----|----|----|----|
| 3 | Charla: Introduccion a Python | Charla | Bogota | 2025-12-20 | user_id 2 (organizador) |
| 4 | Conferencia: Tendencias en IA 2025 | Conferencia | Medellin | 2025-12-22 | user_id 2 |
| 5 | Taller: Git y Control de Versiones | Taller | Palmira | 2025-12-25 | user_id 2 |
| 6 | Seminario: Seguridad en Aplicaciones Web | Seminario | Manizales | 2025-12-28 | user_id 2 |
| 7 | Mesa Redonda: Carrera en Tech | Mesa redonda | Bogota | 2025-12-30 | user_id 2 |
| 8 | Charla: Testing Automatizado | Charla | Medellin | 2025-12-31 | user_id 2 |
| 9 | Taller: React Fundamentals | Taller | Manizales | 2026-01-10 | user_id 2 |
| 10 | Conferencia: Cloud Computing | Conferencia | Palmira | 2026-01-15 | user_id 2 |
| 11 | Seminario: Emprendimiento Tech | Seminario | Bogota | 2026-01-20 | user_id 2 |
| 12 | Mesa Redonda: Etica en IA | Mesa redonda | Manizales | 2026-01-25 | user_id 2 |

## Como Usar

### Opcion 1: PowerShell (Windows)

1. Abre PowerShell en la carpeta del proyecto
2. Ejecuta:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\insert_test_events.ps1
   ```

### Opcion 2: Bash (Linux/Mac)

1. Abre una terminal en la carpeta del proyecto
2. Dale permisos de ejecucion al script:
   ```bash
   chmod +x insert_test_events.sh
   ```
3. Ejecuta:
   ```bash
   ./insert_test_events.sh
   ```

### Opcion 3: Ejecutar SQL directamente

Si tienes psql instalado:

```bash
psql -U postgres -d quercus_db -c "
INSERT INTO event (title, description, date, time, location, category, capacity, organizer_id, status)
VALUES (
  'PRUEBA - Charla: Introduccion a Python',
  'Una charla introductoria sobre los fundamentos de Python.',
  '2025-12-20',
  '10:00',
  'Bogota',
  'Charla',
  50,
  2,
  'activo'
);
"
```

## Sedes Disponibles

La vista de Eventos solo muestra estas 4 sedes:
- Bogota
- Medellin
- Palmira
- Manizales

## Tipos de Eventos

Los eventos se pueden filtrar por estos tipos:
- Charla
- Conferencia
- Taller
- Seminario
- Mesa redonda

## Pruebas con Diferentes Roles

### Como Estudiante (user_id 3)
- Puede ver todos los eventos en la vista de "Eventos"
- Puede registrarse en cualquier evento
- Sus registros aparecen en "Mis Eventos"
- En "Mensajes" solo ve sus propias acciones

### Como Organizador (user_id 2)
- Puede ver todos los eventos
- Los eventos creados por este usuario aparecen en su dashboard de estadisticas
- En "Estadisticas" ve:
  - Cantidad de eventos creados
  - Total de inscripciones en sus eventos
  - Total de asistencias confirmadas
  - Ubicaciones con mas eventos
  - Opcion para descargar PDF con estadisticas
- En "Mensajes" ve:
  - Sus propias acciones
  - Acciones relacionadas con sus eventos (registros, cancelaciones, etc.)

### Como Admin (user_id 1)
- Acceso completo a todas las vistas
- En "Estadisticas" ve sus estadisticas (eventos creados)
- En "Mensajes" ve TODAS las acciones del sistema

## Verificar los Eventos

Para listar los eventos de prueba insertados, ejecuta:

```bash
psql -U postgres -d quercus_db -c "SELECT event_id, title, date, location, category FROM event WHERE title LIKE 'PRUEBA%' ORDER BY date;"
```

## Notas Importantes

- Todos los eventos tienen estado 'activo'
- Los eventos estan marcados con 'PRUEBA-' en el titulo para identificarlos facilmente
- El organizador de todos los eventos es user_id 2
- Los eventos tienen diferentes capacidades (entre 30 y 100 lugares)
- Las fechas van desde diciembre 2025 hasta enero 2026

## Limpiar Eventos de Prueba

Para eliminar todos los eventos de prueba:

```bash
psql -U postgres -d quercus_db -c "DELETE FROM event WHERE title LIKE 'PRUEBA%';"
```

ADVERTENCIA: Esto tambien eliminara los registros asociados si hay foreign keys configuradas.
