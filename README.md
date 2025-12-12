# QUERCUS - Plataforma de Gestión de Eventos UNAL 🌳

Una aplicación web moderna para la gestión completa de eventos universitarios en la Universidad Nacional de Colombia.

---

## 📖 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Características Principales](#características-principales)
- [Arquitectura del Proyecto](#arquitectura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
  - [1. Configurar PostgreSQL](#1-configurar-postgresql)
  - [2. Clonar y Configurar el Proyecto](#2-clonar-y-configurar-el-proyecto)
  - [3. Configurar Variables de Entorno](#3-configurar-variables-de-entorno)
  - [4. Crear la Base de Datos](#4-crear-la-base-de-datos)
  - [5. Instalar Dependencias](#5-instalar-dependencias)
  - [6. Ejecutar la Aplicación](#6-ejecutar-la-aplicación)
- [Uso de la Aplicación](#uso-de-la-aplicación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Base de Datos](#base-de-datos)
- [API/Endpoints](#apiendpoints)
- [Seguridad](#seguridad)
- [Troubleshooting](#troubleshooting)

---

## Descripción General

**QUERCUS** es una plataforma de gestión de eventos universitarios diseñada para la comunidad UNAL. Permite a estudiantes y organizadores:

- 📝 Registrarse e iniciar sesión con credenciales institucionales (@unal.edu.co)
- 📅 Crear y gestionar eventos académicos
- 🎫 Inscribirse y des-inscribirse de eventos
- 📊 Generar reportes y estadísticas
- 🔐 Control de acceso y roles de usuario
- 🔲 Códigos QR para validación de asistencia
- 🔔 Sistema de notificaciones

**Stack Tecnológico:**
- Backend: Flask (Python)
- Base de Datos: PostgreSQL
- Frontend: HTML5, CSS3, JavaScript (Jinja2 templates)
- ORM: SQLAlchemy

---

## Características Principales

✅ **Autenticación Institucional**: Solo usuarios con correo @unal.edu.co  
✅ **Gestión de Roles**: Estudiante, Organizador, Administrador  
✅ **Generación de QR**: Códigos únicos por inscripción  
✅ **Control de Acceso**: Registro de login/logout  
✅ **Sistema de Pagos**: Infraestructura para transacciones  
✅ **Notificaciones**: Sistema de alertas y mensajes  
✅ **Reportes**: Estadísticas de eventos y asistencia  

---

## Arquitectura del Proyecto

```
QUERCUS
├── 🔧 BACKEND
│   ├── app.py                    # Aplicación principal (Flask)
│   ├── models.py                 # Modelos de BD (SQLAlchemy ORM)
│   ├── events.py                 # Lógica de eventos
│   ├── users.py                  # Gestión de usuarios (legacy)
│   ├── quercus_db.sql           # Scripts SQL
│   └── requirements.txt          # Dependencias Python
│
├── 🎨 FRONTEND
│   ├── templates/                # Archivos HTML (Jinja2)
│   │   ├── index.html           # Página principal
│   │   ├── login.html           # Inicio de sesión
│   │   ├── register.html        # Registro de usuarios
│   │   ├── menu.html            # Menú principal
│   │   ├── eventos.html         # Listado de eventos
│   │   ├── mis_eventos.html     # Eventos del usuario
│   │   ├── inscritos_evento.html# Lista de inscritos
│   │   ├── horarios.html        # Calendario/horarios
│   │   ├── alertas.html         # Centro de notificaciones
│   │   ├── success.html         # Páginas de confirmación
│   │   └── emails/              # Templates de emails
│   │
│   └── static/                   # Recursos estáticos
│       ├── css/
│       │   └── style.css        # Estilos globales
│       ├── js/                  # Scripts JavaScript
│       ├── img/
│       │   ├── alertas/         # Íconos de alertas
│       │   ├── avatares/        # Fotos de perfil
│       │   └── eventos/         # Imágenes de eventos
│       └── qr/                  # Códigos QR generados
│
├── 📦 OTROS
├── instance/                     # Archivos de instancia (no commitear)
├── __pycache__/                  # Caché Python
└── docs/                         # Documentación adicional
```

### Separación Backend/Frontend

**BACKEND** (Lógica del servidor)
- `app.py`: Define rutas, lógica de autenticación, generación de QR
- `models.py`: Define estructura de datos
- `events.py`: Funciones de negocio para eventos
- `quercus_db.sql`: Scripts para inicializar BD

**FRONTEND** (Interfaz de usuario)
- `templates/`: Renderizado HTML con Jinja2
- `static/css/`: Estilos CSS
- `static/js/`: Interactividad JavaScript
- `static/img/`: Imágenes y QR generados

---

## Requisitos Previos

### Software Obligatorio

- **Python 3.8+** ([descargar](https://www.python.org/downloads/))
- **PostgreSQL 12+** ([descargar](https://www.postgresql.org/download/))
- **pip** (generalmente viene con Python)
- **Git** (opcional, para clonar el repositorio)

### Verificar instalación

```bash
python --version      # Se estuvo desarrollando en 3.12
pip --version         # Verificar pip
psql --version        # Se desarrollo en 18.1
```

---

## Instalación

### 1. Configurar PostgreSQL

#### En Windows:

1. **Descargar e instalar PostgreSQL:**
   - Ir a https://www.postgresql.org/download/windows/
   - Descargar PostgreSQL 15+ (o la versión estable recomendada)
   - Ejecutar el instalador `.exe`

2. **Durante la instalación:**
   - Anotar la **contraseña del usuario `DAZhzd79`**
   - Puerto por defecto: **5432** (dejar como está)
   - Aceptar todas las opciones por defecto

3. **Verificar la instalación:**
   ```bash
   psql --version
   psql -U postgres
   ```
   - Si pide contraseña, ingresa la que anotaste
   - Escribe `\q` para salir

#### En macOS:

```bash
# Usando Homebrew
brew install postgresql@15

# Iniciar el servicio
brew services start postgresql@15

# Verificar
psql --version
```

#### En Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib

# Verificar
psql --version
```

---

### 2. Clonar y Configurar el Proyecto

```bash
# Clonar el repositorio (si está en Git)
git clone https://github.com/JJossa/quercus_project.git
cd quercus_project


```

---

### 3. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# .env
DB_USER=postgres
DB_PASSWORD=tu_contraseña_postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=quercus_db
FLASK_ENV=development
SECRET_KEY=cambia-esto-por-algo-muy-secreto-y-aleatorio
```

**⚠️ IMPORTANTE:**
- Guarda este archivo en `.gitignore` (no commitear credenciales)
- Cambia el `SECRET_KEY` por algo seguro y aleatorio

---

### 4. Crear la Base de Datos

```bash
# Abrir psql como usuario postgres
psql -U postgres

# En la consola psql, ejecutar:
CREATE DATABASE quercus_db;
\c quercus_db
```

Luego ejecutar el script SQL:

```bash
# Desde la terminal (fuera de psql)
psql -U postgres -d quercus_db -f quercus_db.sql
```

Verificar que las tablas se crearon:

```bash
psql -U postgres -d quercus_db
# Dentro de psql:
\dt  # Listar tablas
```

Deberías ver:
```
Schema |        Name         | Type  | Owner
--------+---------------------+-------+----------
 public | access_control      | table | postgres
 public | event               | table | postgres
 public | notification        | table | postgres
 public | payment             | table | postgres
 public | registration        | table | postgres
 public | report              | table | postgres
 public | role                | table | postgres
 public | users               | table | postgres
```

---

### 5. Instalar Dependencias

```bash
# Crear un entorno virtual (recomendado)
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

**Archivos generados:**
- `venv/` - Entorno virtual aislado

---

### 6. Ejecutar la Aplicación

```bash
# Asegúrate de que el entorno virtual esté activado
# En Windows: venv\Scripts\activate
# En macOS/Linux: source venv/bin/activate

# Ejecutar Flask
python app.py

# La aplicación estará disponible en:
# http://localhost:5000
```

---

## Uso de la Aplicación

### Primer Acceso

1. **Crear cuenta:**
   - Ir a `http://localhost:5000/register`
   - Usuario: Tu nombre (ej: "Juan Pérez")
   - Correo: Tu email institucional (ej: "jperez@unal.edu.co")
   - Contraseña: Mínimo 6 caracteres

2. **Iniciar sesión:**
   - Ir a `http://localhost:5000/login`
   - Usuario/Correo: El correo que usaste
   - Contraseña: La que creaste

3. **Navegar la plataforma:**
   - **Eventos**: Ver todos los eventos disponibles
   - **Mis Eventos**: Ver eventos en los que estás inscrito
   - **Horarios**: Calendario de eventos
   - **Alertas**: Notificaciones del sistema

---

## Base de Datos

### Tablas Principales

#### `users`
Información de usuarios de la plataforma.
```
user_id (PK)    → Identificador único
name            → Nombre del usuario
email           → Email institucional (UNIQUE)
password        → Contraseña
role_id (FK)    → Rol del usuario (estudiante, organizador, admin)
```

#### `role`
Roles y permisos del sistema.
```
role_id (PK)    → Identificador único
role_name       → Nombre del rol
permissions     → Descripción de permisos
```

#### `event`
Eventos creados en la plataforma.
```
event_id (PK)   → Identificador único
title           → Nombre del evento
description     → Descripción
date            → Fecha del evento
time            → Hora del evento
location        → Lugar de realización
category        → Categoría (Académico, Social, etc.)
capacity        → Número máximo de inscritos
status          → Estado (activo, cancelado, finalizado)
```

#### `registration`
Inscripciones de usuarios a eventos.
```
registration_id (PK)   → Identificador único
user_id (FK)           → Usuario inscrito
event_id (FK)          → Evento
registration_date      → Fecha de inscripción
status                 → Estado (confirmado, pendiente, cancelado)
qr_code                → Código QR único
```

#### `access_control`
Registro de accesos al sistema.
```
access_id (PK)    → Identificador único
user_id (FK)       → Usuario
login_time         → Hora de entrada
logout_time        → Hora de salida
token              → Token de sesión
```

#### Otras tablas:
- **`payment`**: Información de pagos y transacciones
- **`notification`**: Notificaciones del sistema
- **`report`**: Reportes de eventos

### Relaciones

```
users ──→ role (muchos a uno)
users ──→ registration (uno a muchos)
users ──→ access_control (uno a muchos)

event ──→ registration (uno a muchos)
event ──→ notification (uno a muchos)
event ──→ report (uno a muchos)

registration ──→ payment (uno a muchos)
```

---

## API/Endpoints

### Autenticación

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET/POST | `/login` | Iniciar sesión |
| GET/POST | `/register` | Crear nueva cuenta |
| GET | `/logout` | Cerrar sesión |

### Eventos

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/eventos` | Listar todos los eventos |
| POST | `/create_event` | Crear evento (organizador) |
| GET | `/mis_eventos` | Ver eventos del usuario |
| GET | `/evento/<id>` | Ver detalles del evento |

### Inscripciones

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/inscribir_evento` | Inscribirse a evento |
| POST | `/desuscribirse` | Desuscribirse de evento |
| GET | `/inscritos_evento/<id>` | Ver inscritos (organizador) |

### Generales

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Página principal |
| GET | `/menu` | Menú principal (requiere sesión) |
| GET | `/horarios` | Calendario de eventos |
| GET | `/alertas` | Centro de notificaciones |

---

## Troubleshooting

### Error: `psycopg2.OperationalError: FATAL: role "postgres" does not exist`

```bash
# Windows: Reinstala PostgreSQL y anota la contraseña
# macOS/Linux:
sudo -u postgres psql
CREATE ROLE postgres WITH SUPERUSER CREATEDB CREATEROLE LOGIN PASSWORD 'tu_contraseña';
```

### Error: `ModuleNotFoundError: No module named 'flask'`

```bash
# Asegúrate de activar el entorno virtual:
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Instala dependencias:
pip install -r requirements.txt
```

### Error: `database "quercus_db" does not exist`

```bash
psql -U postgres
CREATE DATABASE quercus_db;
\c quercus_db
\i quercus_db.sql
```

### La aplicación no carga (puerto en uso)

```bash
# Cambiar puerto en app.py
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Cambiar 5000 a 5001
```

### Error al generar QR

```bash
# Verifica que la carpeta exista
mkdir static/qr

# Verifica permisos de escritura

---

## Contacto y Soporte

Para preguntas o reportar bugs:
- 📧 Email: [jjossa@unal.edu.co]
- 📋 Issues: [GitHub Issues]
- 💬 Discussions: [GitHub Discussions]

---

## Licencia

Este proyecto es parte de la asignatura **Ingeniería de Software II** (2025-2) de la Universidad Nacional de Colombia.

---

**Última actualización:** Diciembre 12, 2025
