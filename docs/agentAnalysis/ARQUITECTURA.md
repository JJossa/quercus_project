# 🏗️ ARQUITECTURA Y DIAGRAMAS DE QUERCUS

Visualización detallada de la arquitectura del proyecto.

---

## 1. DIAGRAMA GENERAL DE LA ARQUITECTURA

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO FINAL                            │
│                     (Navegador Web - HTTP)                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ↓ HTTP Request/Response
        ┌────────────────────────────────────┐
        │     FRONTEND (Presentación)        │
        │                                    │
        │  ├─ templates/                    │
        │  │  ├─ index.html               │
        │  │  ├─ login.html               │
        │  │  ├─ eventos.html             │
        │  │  └─ ... (8 templates más)    │
        │  │                              │
        │  └─ static/                      │
        │     ├─ css/style.css            │
        │     ├─ js/[scripts]             │
        │     ├─ img/{alertas,avatares}  │
        │     └─ qr/{códigos generados}  │
        │                                  │
        └────────────────┬─────────────────┘
                         │ (Jinja2 Rendering)
                         │ (Static Files)
        ┌────────────────────────────────────┐
        │     BACKEND (Lógica de Negocios)  │
        │                                    │
        │  ┌─ app.py (Flask App)           │
        │  │  ├─ @app.route('/login')      │
        │  │  ├─ @app.route('/register')   │
        │  │  ├─ @app.route('/eventos')    │
        │  │  ├─ @app.route('/inscribir')  │
        │  │  └─ generar_qr()              │
        │  │                               │
        │  ├─ models.py (SQLAlchemy ORM)  │
        │  │  ├─ class User               │
        │  │  ├─ class Event              │
        │  │  ├─ class Registration       │
        │  │  ├─ class Payment            │
        │  │  ├─ class Notification       │
        │  │  ├─ class Report             │
        │  │  ├─ class Role               │
        │  │  └─ class AccessControl      │
        │  │                              │
        │  └─ events.py (Business Logic) │
        │     ├─ get_events()            │
        │     ├─ add_event()             │
        │     └─ registrar_usuario_evento()
        │                                  │
        └────────────────┬─────────────────┘
                         │ (SQL Queries)
        ┌────────────────────────────────────┐
        │   DATA LAYER (Persistencia)       │
        │                                    │
        │  ├─ SQLAlchemy (ORM)             │
        │  │                               │
        │  └─ PostgreSQL Database          │
        │     ├─ role                      │
        │     ├─ users                     │
        │     ├─ event                     │
        │     ├─ registration              │
        │     ├─ payment                   │
        │     ├─ notification              │
        │     ├─ report                    │
        │     └─ access_control            │
        │                                  │
        └────────────────────────────────────┘
```

---

## 2. FLUJO DE DATOS (Request/Response)

### Ejemplo: Usuario Inicia Sesión

```
USUARIO
   │
   ├─→ Va a http://localhost:5000/login
   │
   ├─→ Frontend (login.html)
   │   └─→ Renderiza formulario de login
   │
   └─→ Completa y envía:
       {usuario: "jperez@unal.edu.co", contrasena: "miPass123"}
       
       └─→ POST /login
           │
           ├─→ app.py:login() recibe request
           │
           ├─→ Valida:
           │   ├─ Campos no vacíos
           │   ├─ Email termina en @unal.edu.co
           │   └─ Contraseña coincide
           │
           ├─→ Busca en BD:
           │   └─ User.query.filter_by(email=usuario).first()
           │
           ├─→ Verifica contraseña:
           │   └─ check_password_hash(user.password, contrasena)
           │
           ├─→ Si es correcto:
           │   ├─ Crea sesión: session['user_id'] = user.user_id
           │   ├─ Registra acceso en access_control
           │   └─ Redirige a /menu
           │
           └─→ Si es incorrecto:
               └─ Vuelve a login.html con error

RESPUESTA
   │
   ├─→ Frontend (menu.html o login.html)
   │
   └─→ Usuario ve página actualizada
```

---

## 3. DIAGRAMA DE BASE DE DATOS (Entidad-Relación)

```
┌──────────────┐
│    role      │
├──────────────┤
│ role_id (PK) │
│ role_name    │
│ permissions  │
└──┬───────────┘
   │ 1
   │ (role_id)
   │
   │ N
┌──┴───────────────────┐
│      users           │
├──────────────────────┤
│ user_id (PK)         │
│ name                 │
│ email (UNIQUE)       │
│ password             │
│ role_id (FK) ────────┘
├──────────────────────┤
│ ↓ 1:N              │
│ registrations        │
│ access_control       │
│ notifications        │
└─┬────────────────────┘
  │
  │ 1 (user_id)
  │
  │ N
┌─┴──────────────────────┐      ┌──────────────┐
│   registration         │ ──→ │   payment    │
├────────────────────────┤ 1:N ├──────────────┤
│ registration_id (PK)   │      │ payment_id   │
│ user_id (FK) ──────────┘      │ amount       │
│ event_id (FK) ────────┐       │ status       │
│ registration_date     │       │ trans_date   │
│ status                │       │ reference    │
│ qr_code               │       └──────────────┘
└───────┬───────────────┘
        │ 1 (event_id)
        │
        │ N
┌───────┴───────────────────┐
│      event                │
├───────────────────────────┤
│ event_id (PK)             │
│ title                     │
│ description               │
│ date                      │
│ time                      │
│ location                  │
│ category                  │
│ capacity                  │
│ status                    │
├───────────────────────────┤
│ ↓ 1:N                   │
│ notifications             │
│ reports                   │
└───────────────────────────┘

┌──────────────────────┐
│  access_control      │
├──────────────────────┤
│ access_id (PK)       │
│ user_id (FK) ────────→ users
│ login_time           │
│ logout_time          │
│ token                │
└──────────────────────┘

┌──────────────────────┐
│   notification       │
├──────────────────────┤
│ notification_id (PK) │
│ user_id (FK) ────────→ users
│ event_id (FK) ───────→ event
│ message              │
│ type                 │
│ sent_at              │
└──────────────────────┘

┌──────────────────────┐
│      report          │
├──────────────────────┤
│ report_id (PK)       │
│ event_id (FK) ───────→ event
│ total_registrations  │
│ confirmed_attendance │
│ total_payments       │
│ generated_at         │
└──────────────────────┘
```

---

## 4. COMPONENTES PRINCIPALES

### Frontend Components

```
├── Templates (HTML + Jinja2)
│   ├── index.html               → Landing/Home page
│   │   └── Presenta la plataforma
│   │
│   ├── login.html               → Autenticación
│   │   └── Formulario de login
│   │
│   ├── register.html            → Registro de usuarios
│   │   └── Formulario de registro
│   │
│   ├── menu.html                → Menú principal (requiere sesión)
│   │   └── Navegación a todas las secciones
│   │
│   ├── eventos.html             → Listado de eventos disponibles
│   │   └── Muestra todos los eventos + filtros
│   │
│   ├── mis_eventos.html         → Eventos del usuario
│   │   └── Eventos donde está inscrito + QR
│   │
│   ├── inscritos_evento.html   → Gestión de inscritos
│   │   └── Para organizadores: ver quién está inscrito
│   │
│   ├── horarios.html            → Calendario/Horarios
│   │   └── Vista de eventos por fecha/hora
│   │
│   ├── alertas.html             → Centro de notificaciones
│   │   └── Alertas del sistema + mensajes
│   │
│   ├── success.html             → Páginas de confirmación
│   │   └── Confirmaciones de acciones
│   │
│   └── emails/                  → Templates de email
│       └── Correos de confirmación, etc.
│
└── Static Files
    ├── css/
    │   └── style.css            → Estilos CSS globales
    │
    ├── js/
    │   └── [scripts]            → JavaScript para interactividad
    │
    ├── img/
    │   ├── alertas/             → Íconos de alertas
    │   ├── avatares/            → Fotos de perfil usuarios
    │   └── eventos/             → Imágenes de eventos
    │
    └── qr/
        └── [códigos]            → QR generados dinámicamente
```

### Backend Components

```
app.py (Orquestador Principal)
├── Importa modules
├── Configura Flask + SQLAlchemy
├── Define rutas (@app.route)
│   ├── GET /                       → Página principal
│   ├── GET/POST /login            → Autenticación
│   ├── GET/POST /register         → Registro
│   ├── GET /logout                → Cierre de sesión
│   ├── GET /menu                  → Menú principal
│   ├── GET /eventos               → Listar todos
│   ├── POST /create_event         → Crear evento
│   ├── GET /mis_eventos           → Eventos del usuario
│   ├── POST /inscribir_evento     → Inscripción
│   ├── POST /desuscribirse        → Desuscripción
│   ├── GET /inscritos_evento/<id> → Ver inscritos
│   ├── GET /horarios              → Calendario
│   ├── GET /alertas               → Notificaciones
│   └── generar_qr_para_registro() → Generación de QR
├── Decoradores
│   └── @require_roles()           → Control de acceso por rol
└── Context Processors
    └── Variables globales para templates

models.py (Esquema de Datos)
├── db = SQLAlchemy()              → Inicializador ORM
├── class Role                     → Roles (admin, organizador, estudiante)
├── class User                     → Usuarios
│   └── Relaciones: role, registrations, notifications, access_entries
├── class Event                    → Eventos
│   ├── Método: to_dict()         → Serialización a JSON
│   └── Relaciones: registrations, notifications, reports
├── class Registration            → Inscripciones usuario-evento
│   └── Relaciones: user, event, payments
├── class Payment                 → Pagos
│   └── Relación: registration
├── class Notification            → Alertas/Mensajes
│   └── Relaciones: user, event
├── class Report                  → Reportes de eventos
│   └── Relación: event
└── class AccessControl           → Auditoría de accesos
    └── Relación: user

events.py (Lógica de Negocio)
├── eventos = [...]               → Lista en-memoria (CONFLICTO)
├── registros = [...]             → Registros en-memoria
├── get_events()                 → Obtiene eventos
├── add_event()                  → Crea nuevo evento
├── get_registros()              → Obtiene todos los registros
├── registrar_usuario_evento()   → Inscribe usuario a evento
├── obtener_eventos_usuario()    → Eventos del usuario
├── desregistrar_usuario()       → Desuscribe usuario
├── usuario_registrado_en_evento()→ Verifica inscripción
└── _persist_autogen()           → Persiste cambios en archivo

quercus_db.sql (Scripts SQL)
├── DROP TABLE ... CASCADE          → Limpia BD
├── CREATE TABLE role              → Tabla de roles
├── CREATE TABLE users             → Tabla de usuarios
├── CREATE TABLE event             → Tabla de eventos
├── CREATE TABLE registration      → Tabla de inscripciones
├── CREATE TABLE payment           → Tabla de pagos
├── CREATE TABLE notification      → Tabla de notificaciones
├── CREATE TABLE report            → Tabla de reportes
├── CREATE TABLE access_control    → Tabla de auditoría
└── INSERT INTO event ... (ejemplos)
```

---

## 5. CICLO DE VIDA DE UN EVENTO

```
                    CREAR EVENTO
                         │
                         ↓
        1. Organizador accede a /create_event
        2. Completa formulario (título, fecha, capacidad, etc.)
        3. POST /create_event en app.py
        4. Se crea new Event() en models.py
        5. db.session.add() + db.session.commit()
        6. Se inserta en tabla 'event' de PostgreSQL
        7. Redirige a eventos.html con confirmación
                         │
                         ↓
                  EVENTO PUBLICADO
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ↓              ↓              ↓
    USUARIO VE    USUARIO SE    REPORTES
    EN LISTA    INSCRIBE
          │              │              │
          ↓              ↓              ↓
    eventos.html   POST /inscribir   Genera
    muestra en           │           stats
    listado              ↓
                  1. Crear Registration
                  2. user_id + event_id
                  3. Generar QR
                  4. Guardar en BD
                  5. Agregar a mis_eventos.html
                         │
                         ↓
                 DÍA DEL EVENTO
                         │
                         ↓
              Leer QR → Confirmar asistencia
              Update registration.status = 'confirmado'
                         │
                         ↓
                GENERAR REPORTE
                         │
                         ↓
              INSERT INTO report:
              - total_registrations
              - confirmed_attendance
              - total_payments
              - generated_at
```

---

## 6. FLUJO DE AUTENTICACIÓN

```
USUARIO ABRE NAVEGADOR
         │
         ↓
   http://localhost:5000
         │
         ├─→ ¿Hay sesión activa?
         │   (session.get('user_id'))
         │
         ├─ SÍ → Redirige a /menu
         │
         └─ NO → Muestra index.html
                  ├─ "Iniciar Sesión" → /login
                  └─ "Registrarse" → /register

REGISTRO (/register)
         │
         ├─ POST con:
         │  ├─ usuario (nombre)
         │  ├─ correo (@unal.edu.co)
         │  └─ contrasena
         │
         ├─ Validaciones:
         │  ├─ Campos no vacíos
         │  ├─ Contraseña == confirmar
         │  ├─ Email termina en @unal.edu.co
         │  └─ No exista usuario/email
         │
         ├─ Si OK:
         │  ├─ new User()
         │  ├─ Hash contraseña
         │  ├─ db.session.add()
         │  ├─ db.session.commit()
         │  └─ Redirige a /login
         │
         └─ Si error:
            └─ Muestra register.html con error

LOGIN (/login)
         │
         ├─ POST con:
         │  ├─ usuario (email)
         │  └─ contrasena
         │
         ├─ Busca User por email
         │  └─ User.query.filter_by(email=usuario).first()
         │
         ├─ Verifica contraseña
         │  └─ check_password_hash(user.password, contrasena)
         │
         ├─ Si OK:
         │  ├─ session['user_id'] = user.user_id
         │  ├─ session['usuario'] = user.name
         │  ├─ session['email'] = user.email
         │  ├─ session['role_id'] = user.role_id
         │  ├─ Crear AccessControl (auditoría)
         │  ├─ session['access_id'] = acceso.access_id
         │  └─ Redirige a /menu
         │
         └─ Si error:
            └─ Muestra login.html con error

EN /menu (Protegido)
         │
         ├─ @require_roles(['estudiante', 'organizador', 'admin'])
         │
         ├─ Valida sesión
         │  └─ session.get('user_id')
         │
         └─ Renderiza menu.html con datos del usuario
            └─ {usuario: session['usuario'], role: session['role_name']}

LOGOUT (/logout)
         │
         ├─ GET /logout
         │
         ├─ Busca AccessControl por access_id
         │  └─ AccessControl.query.get(access_id)
         │
         ├─ Set logout_time = NOW()
         │  └─ db.session.commit()
         │
         ├─ session.clear()
         │
         └─ Redirige a /login
```

---

## 7. MATRÍZ DE DEPENDENCIAS

```
app.py
  ├─ imports models.py
  │   └─ imports Flask-SQLAlchemy
  │       └─ PostgreSQL
  │
  ├─ imports events.py
  │   └─ lista en-memoria (eventos)
  │
  ├─ imports qrcode
  │   └─ genera PNG en static/qr/
  │
  ├─ imports Flask
  │   └─ renderiza templates/
  │       └─ accede a static/ (CSS, JS, IMG)
  │
  └─ requiere .env
      └─ variables de entorno (DB, SECRET_KEY)

models.py
  ├─ imports SQLAlchemy
  │   └─ conecta a PostgreSQL
  │
  └─ define ORM classes
      └─ usadas por app.py

quercus_db.sql
  └─ crea tablas en PostgreSQL
     └─ mappeadas a classes en models.py
```

---

## 8. TECNOLOGÍAS POR CAPA

```
┌─ PRESENTACIÓN (Frontend) ──────────────────┐
│                                             │
│  HTML5          Jinja2 Templates           │
│  CSS3           style.css                  │
│  JavaScript     vanilla o librería         │
│  QR Images      Generadas dinámicamente    │
│                                             │
└─────────────────────────────────────────────┘
             ↓
        Flask routes
             ↓
┌─ LÓGICA DE NEGOCIOS (Backend) ────────────┐
│                                             │
│  Python 3.8+    Lenguaje principal         │
│  Flask          Framework web              │
│  SQLAlchemy     ORM (Object-Relational)   │
│  werkzeug       Seguridad (hash)           │
│  qrcode         Generación de QR          │
│  Pillow         Manipulación de imágenes  │
│                                             │
└─────────────────────────────────────────────┘
             ↓
        SQL queries
             ↓
┌─ PERSISTENCIA (Data Layer) ────────────────┐
│                                             │
│  PostgreSQL     Base de datos              │
│  Psycopg2       Conector Python ↔ PgSQL   │
│                                             │
│  Tablas:                                   │
│  ├─ users                                  │
│  ├─ role                                   │
│  ├─ event                                  │
│  ├─ registration                           │
│  ├─ payment                                │
│  ├─ notification                           │
│  ├─ report                                 │
│  └─ access_control                         │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 9. ESTRUCTURA DE CARPETAS DETALLADA

```
quercus_project/
│
├── 📄 app.py                    (680 líneas)
│   └─ Punto de entrada, rutas, lógica principal
│
├── 📄 models.py                 (157 líneas)
│   └─ Definición de clases ORM y esquema
│
├── 📄 events.py                 (103 líneas)
│   └─ Lógica de eventos (en-memoria + BD)
│
├── 📄 users.py                  (Legacy - para eliminar)
│   └─ Gestión de usuarios antigua
│
├── 📄 quercus_db.sql            (135 líneas)
│   └─ Scripts SQL para crear tablas
│
├── 📄 requirements.txt
│   └─ Dependencias Python
│
├── 📂 templates/                (11 archivos HTML)
│   ├── index.html              (Home)
│   ├── login.html              (Login)
│   ├── register.html           (Registro)
│   ├── menu.html               (Menú principal)
│   ├── eventos.html            (Listado eventos)
│   ├── mis_eventos.html        (Mis eventos)
│   ├── inscritos_evento.html   (Gestión)
│   ├── horarios.html           (Calendario)
│   ├── alertas.html            (Notificaciones)
│   ├── success.html            (Confirmación)
│   └── emails/
│       └─ [templates de email]
│
├── 📂 static/                   (Recursos estáticos)
│   ├── css/
│   │   └── style.css           (Estilos principales)
│   │
│   ├── js/
│   │   └─ [scripts]            (Interactividad)
│   │
│   ├── img/
│   │   ├── alertas/            (Íconos)
│   │   ├── avatares/           (Fotos)
│   │   └── eventos/            (Imágenes)
│   │
│   └── qr/
│       └─ [códigos generados]  (QR dinámicos)
│
├── 📂 instance/                 (Archivos de instancia)
│   └─ [archivos runtime]
│
├── 📂 docs/                     (Documentación)
│   └─ [archivos de referencia]
│
├── 📂 __pycache__/              (Cache Python)
│   └─ [bytecode compilado]
│
├── 📄 .env                      (Variables de entorno) ⚠️ NO COMMITEAR
│   └─ Credenciales de BD, SECRET_KEY
│
├── 📄 .env.example              (Template de .env)
│   └─ Para documentar variables necesarias
│
├── 📄 .gitignore
│   └─ Incluir .env
│
├── 📄 README.md                 ✨ NUEVO
│   └─ Documentación del proyecto
│
├── 📄 ANALISIS_PROYECTO.md      ✨ NUEVO
│   └─ Análisis de coherencia
│
└── 📄 GUIA_SEGURIDAD.md         ✨ NUEVO
    └─ Correcciones de seguridad
```

---

## 10. VISTA LÓGICA VS FÍSICA

### Vista Lógica (Concepto)
```
┌─────────────────────────────────────┐
│      PLATAFORMA DE EVENTOS UNAL    │
├─────────────────────────────────────┤
│                                     │
│  Gestionar Eventos                 │
│  ├─ Crear                          │
│  ├─ Editar                         │
│  ├─ Listar                         │
│  └─ Eliminar                       │
│                                    │
│  Gestionar Inscripciones           │
│  ├─ Inscribirse                    │
│  ├─ Desuscribirse                  │
│  ├─ Ver inscritos                  │
│  └─ Generar QR                     │
│                                    │
│  Gestionar Usuarios                │
│  ├─ Registrarse                    │
│  ├─ Login                          │
│  ├─ Asignar roles                  │
│  └─ Control de acceso              │
│                                    │
└─────────────────────────────────────┘
```

### Vista Física (Implementación)
```
Servidor Flask
├─ app.py (680 líneas de código)
├─ models.py (157 líneas, 8 clases)
├─ events.py (103 líneas, 8 funciones)
└─ 11 templates HTML + CSS + JS
        ↕
PostgreSQL Database
├─ 8 tablas
├─ Relaciones 1:N y M:N
└─ ~1000 registros (estimado)
```

---

**Diagrama actualizado:** Diciembre 12, 2025

