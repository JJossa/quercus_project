# Estado Actual del Proyecto QUERCUS

## ✅ Completado

### Limpieza de HTML (Perfil)
- Removidos botones de "Estadísticas" y "Mensajes" del panel de perfil
- El perfil ahora solo muestra: **Configuración** y **Salir**
- Los modales `stats-modal` y `messages-modal` han sido completamente removidos del HTML
- Afectados: `eventos.html`, `menu.html`, `horarios.html`

### Limpieza de JavaScript
- Removidas todas las variables que referencian elementos eliminados:
  - `statsBtn`, `statsModal`, `statsClose`
  - `messagesBtn`, `messagesModal`, `messagesClose`
  - `statsPdfBtn`
- Removidos todos los event listeners asociados
- Removidas las funciones `openStatsModal()` que manejaban estos botones
- Archivos limpios: `eventos.html`, `menu.html`, `horarios.html`

---

## 🚨 CRÍTICO - Requiere Acción Inmediata

### 1. Base de Datos - Falta la columna `organizer_id`
**Error**: `no existe la columna event.organizer_id`

**Causa**: El archivo `quercus_db.sql` define la columna `organizer_id` en la tabla `event`, pero la base de datos PostgreSQL actual NO tiene esta columna.

**Solución**: Recrear la base de datos ejecutando en PowerShell:

```powershell
psql -U postgres -d quercus_db -f quercus_db.sql
```

**Esto hará**:
- Eliminar la BD actual
- Recrearla con todas las columnas incluido `organizer_id`
- Agregar relación foreign key con la tabla `users`

⚠️ **ADVERTENCIA**: Esto eliminará TODOS los datos actuales. Si hay datos importantes, hacer backup primero.

---

## 📝 Por Hacer (En Orden de Prioridad)

### [P1] Recrear Base de Datos
```powershell
psql -U postgres -d quercus_db -f quercus_db.sql
```
- **Estado**: NOT STARTED
- **Bloqueador**: Sin esto, la página de eventos no carga
- **Tiempo estimado**: 2-3 minutos

---

### [P2] Verificar Estructura del Menú
**Pregunta**: ¿Dónde están ubicados los siguientes botones/vistas del menú?
1. **Usuarios** - Crear nueva cuenta
2. **Mis Eventos** - Ver eventos en los que está inscrito
3. **Crear Evento** - Formulario para crear evento
4. **Mensajes** - Actividades/registro de logs (icon: `icono4.png`) ← **AQUÍ va el Activity Log**
5. **Alertas** - Notificaciones/alertas

**Observación**: El botón "Mensajes" ya existe con `icono4.png`, pero al parecer su vista no está implementada. Aquí es donde debería mostrarse el Activity Log en lugar de en un modal del perfil.

**Acción necesaria**: 
- Verificar si existe archivo `templates/mensajes.html` o similar
- Si existe, conectar el endpoint `/api/activity-log` a esa vista
- Si no existe, crear la vista `mensajes.html` con el Activity Log

---

### [P3] Estadísticas en el Menú
**Situación**: El botón "Estadísticas" debe aparecer en el MENÚ PRINCIPAL, no en el perfil.

**Acciones pendientes**:
- [ ] Verificar si existe vista/botón "Estadísticas" en el menú
- [ ] Si no existe, crear `estadisticas.html` con:
  - Tabla de eventos creados
  - Estadísticas de inscripciones
  - Lugares más frecuentes
  - Botón para descargar PDF
- [ ] Conectar endpoint `/api/user/stats` a esta vista
- [ ] Arreglar endpoint `/api/user/stats/pdf` (actualmente no funciona)

---

### [P4] Reparar Descarga de PDF
**Error**: El botón "Descargar PDF" en estadísticas no funciona

**Ubicación**: `app.py` - endpoint `/api/user/stats/pdf` (alrededor de línea 250-280)

**Problema probable**: 
```python
# ❌ INCORRECTO
return send_file(pdf_bytes, mimetype='application/pdf', download_name='stats.pdf')

# ✅ CORRECTO
return send_file(pdf_bytes, mimetype='application/pdf', as_attachment=True, download_name='stats.pdf')
```

**Acción**: Revisar parámetros de `send_file()` y corregir

---

### [P5] Estilo Flotante para Vistas Principales
**Solicitud**: Las vistas de Eventos, Crear Eventos y Alertas deben tener la misma apariencia "flotante" que los modales (config-modal, stats-modal).

**Ubicación**: 
- CSS: `static/css/style.css` - clase `.logout-modal`
- HTML: `templates/eventos.html`, `templates/horarios.html`, `templates/alertas.html`

**Acción**:
1. Identificar qué contenedor es el principal en cada vista
2. Aplicar clase `.logout-modal` o crear wrapper con el mismo estilo
3. Ajustar CSS si es necesario para que se vea como una "tarjeta flotante"

---

## 📊 Estructura del Menú (Información de Referencia)

El menú debería tener 5 opciones principales:

```
┌─────────────────────────────┐
│ PERFIL: [Config] [Salir]    │  ← Solo estos dos botones
├─────────────────────────────┤
│ 1. Usuarios                 │  ← Crear cuenta
│ 2. Mis Eventos              │  ← Eventos registrados
│ 3. Crear Evento             │  ← Formulario + Warning para estudiantes
│ 4. Mensajes (icono4.png)    │  ← Activity Log va AQUÍ
│ 5. Alertas                  │  ← Notificaciones
├─────────────────────────────┤
│ ESTADÍSTICAS (separado)     │  ← Vista independiente para org/admin
└─────────────────────────────┘
```

**No debe haber**:
- ❌ Botones de estadísticas en el perfil
- ❌ Botones de mensajes en el perfil
- ❌ Modales duplicados en el perfil

---

## 🔍 Archivos Modificados Hoy

1. **eventos.html**
   - ✅ Removidos botones `stats-btn` y `messages-btn` (línea 110)
   - ✅ Removidos modales `stats-modal` y `messages-modal` (líneas 149-211)
   - ✅ Removidas variables de estas referencias (línea ~340)
   - ✅ Removidos todos los event listeners (líneas ~340-440)

2. **menu.html**
   - ✅ Removidos botones del perfil (línea 160-166)
   - ✅ Removidas variables (línea ~400-410)
   - ✅ Removidos listeners (línea ~470-540)

3. **horarios.html**
   - ✅ Removidos botones del perfil (línea 88-94)
   - ✅ Removidas variables (línea ~579-590)
   - ✅ Removidos listeners (línea ~595-680)

---

## 🔗 Endpoints Disponibles

### User Profile
- `GET /api/me` - Obtener datos del usuario (name, email, role)
- `POST /api/user/profile` - Actualizar nick y password

### Statistics
- `GET /api/user/stats` - Obtener estadísticas (solo org/admin)
- `GET /api/user/stats/pdf` - Descargar PDF de estadísticas (⚠️ ROTO)

### Activity Log
- `GET /api/activity-log` - Obtener historial de actividades

### Events
- `GET /api/events` - Listar todos los eventos
- `POST /api/event` - Crear evento
- `POST /api/event/<id>/register` - Inscribirse en evento
- `POST /api/event/<id>/unregister` - Desinscribirse de evento

---

## 🎯 Próximos Pasos (En Orden)

1. **AHORA**: Ejecutar `psql -U postgres -d quercus_db -f quercus_db.sql`
2. **Luego**: Probar que la página de eventos carga sin errores
3. **Después**: Identificar estructura del menú y vistas existentes
4. **Luego**: Implementar vista "Mensajes" con Activity Log si no existe
5. **Luego**: Implementar vista "Estadísticas" en menú si no existe
6. **Finalmente**: Reparar PDF y aplicar estilos flotantes

---

**Última actualización**: Hoy - Limpieza de perfil completada
**Estado**: Bloqueado en BD (necesita recreación)
