# 🔒 GUÍA DE CORRECCIONES DE SEGURIDAD

Este documento contiene las correcciones recomendadas para los problemas de seguridad críticos detectados.

---

## 1. IMPLEMENTAR HASH DE CONTRASEÑAS

### Paso 1: Instalar `werkzeug`

```bash
pip install werkzeug
```

Ya está en `requirements.txt` (Werkzeug==3.1.4), pero si no:
```bash
pip install werkzeug==3.1.4
```

### Paso 2: Actualizar `models.py`

Agregar imports:
```python
from werkzeug.security import generate_password_hash, check_password_hash
```

**Archivo original (models.py línea 29):**
```python
class User(db.Model):
    __tablename__ = 'users'
    ...
    password = db.Column(db.Text, nullable=False)
```

**Cambiar a:**
```python
class User(db.Model):
    __tablename__ = 'users'
    ...
    password = db.Column(db.Text, nullable=False)
    
    def set_password(self, plain_password):
        """Hashear contraseña antes de guardar"""
        self.password = generate_password_hash(plain_password, method='pbkdf2:sha256')
    
    def check_password(self, plain_password):
        """Verificar contraseña sin hashear"""
        return check_password_hash(self.password, plain_password)
```

### Paso 3: Actualizar `app.py` - Función `register()`

**Original (app.py línea 169-176):**
```python
nuevo_usuario = User(
    name=usuario,
    email=correo,
    password=contrasena,  # ❌ TEXTO PLANO
    role_id=None
)
```

**Cambiar a:**
```python
nuevo_usuario = User(
    name=usuario,
    email=correo,
    role_id=None
)
nuevo_usuario.set_password(contrasena)  # ✅ HASHEADA
```

### Paso 4: Actualizar `app.py` - Función `login()`

**Original (app.py línea 57-59):**
```python
if user.password != contrasena:  # ❌ COMPARACIÓN DIRECTA
    print("[LOGIN] ✗ Contraseña incorrecta")
    return render_template('login.html', error="Usuario o contraseña incorrectos.")
```

**Cambiar a:**
```python
if not user.check_password(contrasena):  # ✅ COMPARACIÓN CON HASH
    print("[LOGIN] ✗ Contraseña incorrecta")
    return render_template('login.html', error="Usuario o contraseña incorrectos.")
```

---

## 2. USAR VARIABLES DE ENTORNO

### Paso 1: Instalar `python-dotenv`

```bash
pip install python-dotenv
```

Agregar a `requirements.txt`:
```
python-dotenv==1.0.0
```

### Paso 2: Crear archivo `.env`

En la raíz del proyecto (mismo nivel que `app.py`):

```env
# .env
FLASK_ENV=development
FLASK_DEBUG=True

# PostgreSQL
DB_USER=postgres
DB_PASSWORD=tu_contraseña_actual
DB_HOST=localhost
DB_PORT=5432
DB_NAME=quercus_db

# Flask Secret
SECRET_KEY=tu-clave-secreta-muy-aleatoria-y-larga-aqui-12345679890
```

⚠️ **IMPORTANTE:** Agregar `.env` a `.gitignore`:

```bash
# En la raíz del proyecto, agregar a .gitignore
echo ".env" >> .gitignore
```

### Paso 3: Actualizar `app.py`

**Original (app.py línea 1-19):**
```python
import uuid
import os       
import io
import base64
import qrcode
from functools import wraps
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_file

from models import db, User, Role, Event, Registration, Payment, Notification, Report, AccessControl

app = Flask(__name__)

# 🔌 Configuración de conexión a PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:DAZhzd79@localhost:5432/quercus_db'  # ❌ HARDCODED
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Clave para manejar sesiones (login)
app.secret_key = 'cambia-esto-por-algo-muy-secreto'  # ❌ HARDCODED
```

**Cambiar a:**
```python
import uuid
import os
import io
import base64
import qrcode
from functools import wraps
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_file
from dotenv import load_dotenv  # ✅ NUEVO

from models import db, User, Role, Event, Registration, Payment, Notification, Report, AccessControl

# Cargar variables de entorno
load_dotenv()  # ✅ NUEVO

app = Flask(__name__)

# 🔌 Configuración de conexión a PostgreSQL (desde variables de entorno)
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'quercus_db')

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL  # ✅ DESDE VARIABLES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'development')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Clave para manejar sesiones (login)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')  # ✅ DESDE VARIABLES
```

### Paso 4: Crear `.env.example` para documentación

```env
# .env.example (SÍ COMMITEAR ESTO)
# Copiar este archivo a .env y completar con tu información

FLASK_ENV=development
FLASK_DEBUG=True

# PostgreSQL Configuration
DB_USER=postgres
DB_PASSWORD=tu_contraseña_aqui
DB_HOST=localhost
DB_PORT=5432
DB_NAME=quercus_db

# Flask Configuration
SECRET_KEY=cambia-esto-por-una-clave-aleatoria-muy-secreta
```

---

## 3. AGREGAR COLUMNA `time` A MODELS

### En `models.py` línea 52

**Original:**
```python
class Event(db.Model):
    __tablename__ = 'event'

    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200))  # ❌ FALTA time
```

**Cambiar a:**
```python
class Event(db.Model):
    __tablename__ = 'event'

    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time)  # ✅ AGREGADO
    location = db.Column(db.String(200))
```

**Actualizar `to_dict()` también:**
```python
def to_dict(self):
    return {
        "id": self.event_id,
        "titulo": self.title,
        "descripcion": self.description,
        "fecha": self.date.strftime("%Y-%m-%d") if self.date else None,
        "hora": self.time.strftime("%H:%M") if self.time else None,  # ✅ AGREGADO
        "lugar": self.location,
        "categoria": self.category,
        "capacidad": self.capacity,
        "status": self.status,
    }
```

---

## 4. ELIMINAR ARCHIVOS LEGACY

### `users.py` ya no es necesario

Archivo: `users.py`

**Acción:** Eliminar completamente

**Razón:**
- Todo funciona a través de `models.User` + SQLAlchemy
- Mantenerlo causa confusión
- El import en `app.py` está comentado

```bash
# En terminal
rm users.py
```

### Actualizar imports en `app.py`

**Original (app.py línea 8):**
```python
# from users import get_users, add_user  # usar get_users() para leer siempre el estado actual
from events import get_events, add_event, obtener_eventos_usuario, registrar_usuario_evento, desregistrar_usuario
```

**Cambiar a:**
```python
# users.py está deprecated, usar models.User en su lugar
from events import get_events, add_event, obtener_eventos_usuario, registrar_usuario_evento, desregistrar_usuario
```

---

## 5. VALIDACIÓN MEJORADA DE EMAIL

### En `app.py`, agregar función validadora

Agregar después de imports (alrededor de línea 15):

```python
import re

def is_valid_institutional_email(email):
    """Valida que sea un email institucional de UNAL"""
    pattern = r'^[a-zA-Z0-9._%+-]+@unal\.edu\.co$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    """Valida que la contraseña sea fuerte"""
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    if not any(c.isupper() for c in password):
        return False, "La contraseña debe tener al menos una mayúscula"
    if not any(c.isdigit() for c in password):
        return False, "La contraseña debe tener al menos un dígito"
    return True, "Contraseña válida"
```

### Usar en `register()`

**Original (app.py línea 155):**
```python
if not correo.endswith('@unal.edu.co'):
    print(f"[REGISTER] ✗ Correo NO institucional: {correo}")
    return render_template('register.html', error="Solo se permiten correos institucionales @unal.edu.co.")
```

**Cambiar a:**
```python
if not is_valid_institutional_email(correo):
    print(f"[REGISTER] ✗ Correo inválido: {correo}")
    return render_template('register.html', error="Email inválido. Usa tu correo institucional @unal.edu.co")

is_valid, msg = is_strong_password(contrasena)
if not is_valid:
    print(f"[REGISTER] ✗ Contraseña débil: {msg}")
    return render_template('register.html', error=f"Contraseña débil: {msg}")
```

---

## 6. MANEJO DE EXCEPCIONES EN BD

### En `register()`

**Original (app.py línea 177):**
```python
db.session.add(nuevo_usuario)
db.session.commit()
```

**Cambiar a:**
```python
try:
    db.session.add(nuevo_usuario)
    db.session.commit()
except Exception as e:
    db.session.rollback()
    print(f"[ERROR] Al crear usuario: {e}")
    return render_template('register.html', 
        error="Error al crear cuenta. Intenta de nuevo.")
```

### En `login()`

**Original (app.py línea 85):**
```python
db.session.add(acceso)
db.session.commit()
```

**Cambiar a:**
```python
try:
    db.session.add(acceso)
    db.session.commit()
except Exception as e:
    db.session.rollback()
    print(f"[ERROR] Al registrar acceso: {e}")
    # Continuar de todas formas, no es crítico
```

---

## 7. ORDEN DE IMPLEMENTACIÓN RECOMENDADO

### Día 1 (Crítico)
1. ✅ Instalar `werkzeug` y `python-dotenv`
2. ✅ Crear `.env` con credenciales
3. ✅ Actualizar `app.py` para usar variables de entorno
4. ✅ Agregar métodos de hash en `models.User`

### Día 2
5. ✅ Actualizar `register()` para hashear contraseñas
6. ✅ Actualizar `login()` para verificar con hash
7. ✅ Eliminar `users.py` y actualizar imports
8. ✅ Agregar `time` a `models.Event`

### Día 3
9. ✅ Agregar validadores de email y contraseña
10. ✅ Agregar try/except en operaciones de BD
11. ✅ Crear `.env.example`
12. ✅ Agregar `.env` a `.gitignore`

---

## 8. TESTING DE CAMBIOS

### Probar Hash de Contraseñas

```python
# En Python shell
from werkzeug.security import generate_password_hash, check_password_hash

# Generar hash
hash1 = generate_password_hash("mi_contraseña_123", method='pbkdf2:sha256')
print(hash1)  # Algo como: pbkdf2:sha256$XXX$YYY

# Verificar
print(check_password_hash(hash1, "mi_contraseña_123"))    # True
print(check_password_hash(hash1, "contraseña_incorrecta")) # False
```

### Probar Variables de Entorno

```python
# En Python shell, después de crear .env
from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv('DB_USER'))      # postgres
print(os.getenv('DB_PASSWORD'))  # tu_contraseña
print(os.getenv('SECRET_KEY'))   # tu-clave-secreta
```

### Probar Validación de Email

```python
# En Python shell
import re

def is_valid_institutional_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@unal\.edu\.co$'
    return re.match(pattern, email) is not None

print(is_valid_institutional_email("usuario@unal.edu.co"))        # True
print(is_valid_institutional_email("usuario@gmail.com"))          # False
print(is_valid_institutional_email("usuario.apellido@unal.edu.co")) # True
```

---

## 9. CHECKLIST DE VERIFICACIÓN

Después de implementar todos los cambios:

- [ ] `pip install -r requirements.txt` se ejecuta sin errores
- [ ] `.env` existe en la raíz del proyecto
- [ ] `.env` está en `.gitignore`
- [ ] `app.py` usa variables de entorno (no hardcoded)
- [ ] `models.User` tiene métodos `set_password()` y `check_password()`
- [ ] `register()` hashea contraseñas antes de guardar
- [ ] `login()` verifica contraseñas con hash
- [ ] `models.Event` tiene columna `time`
- [ ] `users.py` fue eliminado
- [ ] `app.py` no importa de `users.py`
- [ ] Validadores de email funcionan
- [ ] Try/except agregado en operaciones de BD
- [ ] La aplicación inicia sin errores: `python app.py`
- [ ] Login funciona con la nueva contraseña hasheada
- [ ] Registro de nuevo usuario funciona

---

## 10. REFERENCIAS Y RECURSOS

### Documentación
- [Werkzeug Security](https://werkzeug.palletsprojects.com/en/2.0.x/security/)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [SQLAlchemy Security](https://docs.sqlalchemy.org/)

### Tutoriales Útiles
- [Flask Authentication](https://flask.palletsprojects.com/en/2.0.x/patterns/authentication/)
- [Password Hashing Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

---

**Documento actualizado:** Diciembre 12, 2025

Si tienes dudas o problemas durante la implementación, consulta este documento o los archivos mencionados.
