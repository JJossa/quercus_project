import uuid
import os       #Para codigo QR
import io
import base64
import qrcode
from functools import wraps
from datetime import datetime, date  # para logout
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_file
# from users import get_users, add_user  # usar get_users() para leer siempre el estado actual
from events import get_events, add_event, obtener_eventos_usuario, registrar_usuario_evento, desregistrar_usuario  # endpoints simples para eventos
from models import db, User, Role, Event, Registration, Payment, Notification, Report, AccessControl

app = Flask(__name__)

# 🔌 Configuración de conexión a PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:DAZhzd79@localhost:5432/quercus_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Clave para manejar sesiones (login)
app.secret_key = 'cambia-esto-por-algo-muy-secreto'

# Inicializar SQLAlchemy con la app
db.init_app(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lo que el usuario escribe en el campo "Usuario" del formulario
        usuario = request.form.get('usuario', '').strip()
        contrasena = request.form.get('contrasena', '').strip()

        print(f"[LOGIN] Usuario recibido (campo usuario): '{usuario}'")
        print(f"[LOGIN] Contraseña recibida: '{contrasena}'")

        if not usuario or not contrasena:
            return render_template('login.html', error="Debes ingresar usuario y contraseña.")

        # 👉 Interpretamos "usuario" como CORREO institucional
        if not usuario.endswith('@unal.edu.co'):
            print(f"[LOGIN] ✗ Correo no institucional: {usuario}")
            return render_template('login.html', error="Debes usar tu correo institucional @unal.edu.co.")

        # Buscamos en la BD por EMAIL (columna email de la tabla users)
        user = User.query.filter_by(email=usuario).first()

        if user is None:
            print("[LOGIN] ✗ Usuario (correo) no encontrado en BD")
            return render_template('login.html', error="Usuario o contraseña incorrectos.")

        if user.password != contrasena:
            print("[LOGIN] ✗ Contraseña incorrecta")
            return render_template('login.html', error="Usuario o contraseña incorrectos.")

        # ✅ Login exitoso
        session['user_id'] = user.user_id
        session['usuario'] = user.name   # nombre para mostrar en la app
        session['email'] = user.email    # por si luego lo quieres usar
        
        #Para roles
        session['role_id']   = user.role_id
        session['user_name']  = user.name
        # Si el usuario no tiene rol asociado, asumimos 'estudiante' como rol por defecto
        if user.role and getattr(user.role, "role_name", None):
            session['role_name'] = user.role.role_name   # ✅ columna real
        else:
            session['role_name'] = 'estudiante'
            print(f"[WARN] Usuario {user.email} no tenía rol; usando 'estudiante' por defecto.")




        # 🔹 Registrar acceso en access_control
        access_token = str(uuid.uuid4())   # token simple para esta sesión
        acceso = AccessControl(
            user_id=user.user_id,
            token=access_token
            # login_time se llena solo con datetime.utcnow por el default del modelo
        )
        db.session.add(acceso)
        db.session.commit()

        # Guardar el id del registro de acceso en la sesión
        session['access_id'] = acceso.access_id

        print(f"[LOGIN] ✓ Login exitoso para {user.email}, access_id={acceso.access_id}")
        return redirect(url_for('menu'))

    # GET
    return render_template('login.html')

@app.route('/logout')
def logout():
    user_id   = session.get('user_id')
    access_id = session.get('access_id')

    print(f"[LOGOUT] user_id en sesión: {user_id}")
    print(f"[LOGOUT] access_id en sesión: {access_id}")

    if access_id:
        entry = AccessControl.query.get(access_id)
        print(f"[LOGOUT] entry encontrado: {entry}")

        if entry and entry.logout_time is None:
            entry.logout_time = db.func.now()  # 👈 aquí el cambio
            db.session.commit()
            print(f"[LOGOUT] ✓ logout_time actualizado para access_id={access_id}")

    session.clear()
    return redirect(url_for('login'))

def require_roles(allowed_roles): #Decorador para restringir rutas según rol
    """
    allowed_roles: lista de nombres de rol permitidos, p.ej. ['admin', 'organizador']
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id   = session.get('user_id')
            role_name = session.get('role_name')

            if not user_id:
                # No hay sesión -> al login
                return redirect(url_for('login'))

            if role_name not in allowed_roles:
                # Tiene sesión, pero no el rol correcto
                return "No tienes permisos para acceder a esta funcionalidad.", 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        correo = request.form.get('correo', '').strip()
        contrasena = request.form.get('contrasena', '').strip()
        confirmar = request.form.get('confirmar', '').strip()

        print("========== ENTRO A REGISTER (NUEVA VERSION) ==========")
        print(f"[REGISTER] Usuario: '{usuario}'")
        print(f"[REGISTER] Correo: '{correo}'")
        print(f"[REGISTER] Contraseña: '{contrasena}'")
        print(f"[REGISTER] Confirmar: '{confirmar}'")

        # 1. Validar campos vacíos
        if not usuario or not correo or not contrasena or not confirmar:
            print("[REGISTER] ✗ Campos vacíos")
            return render_template('register.html', error="Todos los campos son obligatorios.")

        # 2. Validar que las contraseñas coincidan
        if contrasena != confirmar:
            print("[REGISTER] ✗ Contraseñas no coinciden")
            return render_template('register.html', error="Las contraseñas no coinciden.")

        # 3. Validar correo institucional
        if not correo.endswith('@unal.edu.co'):
            print(f"[REGISTER] ✗ Correo NO institucional: {correo}")
            return render_template('register.html', error="Solo se permiten correos institucionales @unal.edu.co.")

        # 4. Verificar que no exista ya el nombre o el correo
        existente = User.query.filter(
            (User.name == usuario) | (User.email == correo)
        ).first()

        if existente:
            print("[REGISTER] ✗ Usuario o correo ya existen")
            return render_template('register.html', error="El nombre de usuario o correo ya existen.")

        # 5. Crear el usuario
        nuevo_usuario = User(
            name=usuario,
            email=correo,
            password=contrasena,
            role_id=None
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        print(f"[REGISTER] ✓ Usuario creado en BD con id {nuevo_usuario.user_id}")
        return redirect(url_for('login'))

    # GET
    return render_template('register.html')

# -------------------------
# Helper para generar QR
# -------------------------
def generar_qr_para_registro(registro):
    # 1. Texto que se codifica en el QR
    qr_data = f"registro_id={registro.registration_id};user_id={registro.user_id};event_id={registro.event_id}"

    # 2. Generar imagen PNG en memoria
    img = qrcode.make(qr_data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    png_bytes = buf.getvalue()

    # 3. Convertir a Base64 para guardarlo en la BD
    b64 = base64.b64encode(png_bytes).decode("utf-8")

    # 4. Guardar en el modelo (columna qr_code)
    registro.qr_code = b64


@app.route('/registro/<int:reg_id>/qr')
def qr_registro(reg_id):
    # 1. Buscar el registro
    reg = Registration.query.get_or_404(reg_id)

    # 2. Usar las relaciones hacia usuario y evento
    evento = reg.event          # relación Registration -> Event
    usuario = reg.user          # relación Registration -> User

    # 3. Preparar datos legibles para el QR
    #    (texto que verás al escanear con el celular)
    hora_str = ""
    try:
        if getattr(evento, "time", None):
            hora_str = evento.time.strftime("%H:%M")
    except Exception:
        hora_str = ""

    qr_data = (
        "QUERCUS - Registro de evento\n"
        f"Registro ID: {reg.registration_id}\n"
        f"Estado: {reg.status or 'inscrito'}\n\n"
        f"Evento: {evento.title}\n"
        f"Fecha: {evento.date}"
        + (f" {hora_str}" if hora_str else "") + "\n"
        f"Lugar: {evento.location or '-'}\n"
        f"Categoría: {evento.category or '-'}\n\n"
        f"Usuario: {usuario.name}\n"
        f"Correo: {usuario.email}"
    )

    # (opcional) Ver en consola qué se está metiendo en el QR
    print("[QR] Datos codificados:")
    print(qr_data)

    # 4. Generar la imagen PNG del QR
    img = qrcode.make(qr_data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    # 5. Enviar la imagen como respuesta HTTP
    return send_file(buf, mimetype="image/png")

@app.route('/success')
def success():
    return render_template('success.html')

# 🔹 Nueva ruta del menú principal
@app.route('/menu')
def menu():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    role_name = session.get('role_name', 'estudiante')
    print("[MENU] role_name en sesión =", session.get('role_name'))

    return render_template(
        'menu.html',
        role_name=role_name, 
        es_admin       = (role_name == 'admin'),
        es_organizador = (role_name == 'organizador'),
        es_estudiante  = (role_name == 'estudiante'),
    )


@app.route('/eventos')
def eventos():
    eventos = Event.query.order_by(Event.date).all()
    return render_template('eventos.html', eventos=eventos) 

@app.route('/mis_eventos')
def mis_eventos():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    registros = Registration.query.filter_by(user_id=user_id).all()
    return render_template('mis_eventos.html', registros=registros)



@app.route('/horarios')
@require_roles(['admin', 'organizador'])
def horarios():
    return render_template('horarios.html')

@app.route('/alertas')
def alertas():
    return render_template('alertas.html')

# API mínima para eventos: listar y crear (cliente puede llamar vía fetch/ajax)
@app.route('/api/eventos', methods=['GET'])
def api_get_eventos():
    user_id = session.get('user_id')

    # Trae todos los eventos desde PostgreSQL
    eventos = Event.query.order_by(Event.date).all()

    # Conjunto de ids de eventos en los que el usuario ya está registrado
    if user_id:
        regs = Registration.query.filter_by(user_id=user_id).all()
        registrados_ids = {r.event_id for r in regs}
    else:
        registrados_ids = set()

    payload = []
    for e in eventos:
        d = e.to_dict()              # devuelve id, titulo, fecha, descripcion, etc.
        d['registrado'] = e.event_id in registrados_ids
        payload.append(d)
    
    print("[DEBUG] Payload /api/eventos:")  #Prueba temporal
    for item in payload:
        print(item)

    print(f"[API] GET /api/eventos - {len(payload)} eventos (user_id={user_id})")
    return jsonify(payload)



from datetime import datetime

@app.route('/api/eventos/create', methods=['POST'])
@require_roles(['admin', 'organizador'])
def api_create_evento():
    """Crea un evento en la tabla 'event' a partir de datos JSON o form-data."""

    # 1. Verificar que haya usuario logueado
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "No autenticado"}), 401

    # 2. Leer datos (aceptamos JSON o form-data)
    if request.is_json:
        data = request.get_json() or {}
        titulo      = (data.get('titulo') or '').strip()
        descripcion = (data.get('descripcion') or '').strip()
        fecha_str   = (data.get('fecha') or '').strip()      # se espera 'YYYY-MM-DD'
        hora_str    = data.get('hora')    # 👈 'HH:MM'
        lugar       = (data.get('lugar') or '').strip()
        categoria   = (data.get('categoria') or '').strip()
        capacidad   = data.get('capacidad')
        status      = (data.get('status') or 'activo').strip()
    else:
        titulo      = (request.form.get('titulo') or '').strip()
        descripcion = (request.form.get('descripcion') or '').strip()
        fecha_str   = (request.form.get('fecha') or '').strip()
        hora_str    = request.form.get('hora')
        lugar       = (request.form.get('lugar') or '').strip()
        categoria   = (request.form.get('categoria') or '').strip()
        capacidad   = request.form.get('capacidad')
        status      = (request.form.get('status') or 'activo').strip()

    print(f"[API] POST /api/eventos/create por user_id={user_id} "
          f"- titulo:{titulo}, fecha:{fecha_str}, lugar:{lugar}")

    # 3. Validaciones básicas
    if not titulo or not fecha_str:
        return jsonify({"error": "Título y fecha son obligatorios."}), 400

    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD."}), 400

    # 4. Capacidad opcional pero numérica
    capacidad_val = None
    if capacidad not in (None, ""):
        try:
            capacidad_val = int(capacidad)
        except ValueError:
            return jsonify({"error": "La capacidad debe ser un número entero."}), 400

    
    # 5. Crear el evento y guardar en PostgreSQL
    hora_value = None
    if hora_str:
         try:
              hora_value = datetime.strptime(hora_str, "%H:%M").time()
         except ValueError:
            return jsonify({"error": "Formato de hora inválido. Use HH:MM."}), 400
    nuevo_evento = Event(
        title       = titulo,
        description = descripcion,
        date        = fecha,
        time        = hora_value,
        location    = lugar,
        category    = categoria,
        capacity    = capacidad_val,
        status      = status
    )

    db.session.add(nuevo_evento)
    db.session.commit()

    print(f"[API] Evento creado en BD con id {nuevo_evento.event_id}")

    return jsonify(nuevo_evento.to_dict()), 201

@app.route('/api/eventos/delete', methods=['POST'])
@require_roles(['admin', 'organizador'])
def api_delete_eventos():
    """Elimina uno o varios eventos por ID (lista de ids)."""

    # Verificar que haya usuario autenticado
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "No autenticado"}), 401

    try:
        data = request.get_json() or {}
        ids = data.get('ids', [])

        # Validar que sea una lista no vacía
        if not isinstance(ids, list) or not ids:
            return jsonify({"error": "Lista de ids vacía o inválida"}), 400

        # Limpiar y convertir a enteros
        ids_clean = []
        for i in ids:
            try:
                ids_clean.append(int(i))
            except (TypeError, ValueError):
                pass

        if not ids_clean:
            return jsonify({"error": "No hay ids válidos para eliminar"}), 400

        print(f"[API] /api/eventos/delete solicitado por user_id={user_id} ids={ids_clean}")

        # 1. Eliminar primero las inscripciones (Registration) que dependan de esos eventos
        Registration.query.filter(
            Registration.event_id.in_(ids_clean)
        ).delete(synchronize_session=False)

        # 2. Ahora sí eliminar los eventos
        Event.query.filter(
            Event.event_id.in_(ids_clean)
        ).delete(synchronize_session=False)

        db.session.commit()
        print(f"[API] /api/eventos/delete OK - eliminados {len(ids_clean)} evento(s)")
        return jsonify({"ok": True, "deleted": len(ids_clean)}), 200

    except Exception as e:
        db.session.rollback()
        print("[API] Error eliminando eventos:", repr(e))
        return jsonify({"error": "Error interno al eliminar eventos"}), 500

@app.route('/api/eventos/<int:event_id>/update', methods=['PUT'])
def api_update_evento(event_id):
    """Actualiza un evento existente."""

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "No autenticado"}), 401

    evento = Event.query.get(event_id)
    if not evento:
        return jsonify({"error": "Evento no encontrado"}), 404

    data = request.get_json() or {}

    # Leer campos (si vienen, se actualizan; si no, se dejan igual)
    titulo      = (data.get('titulo') or '').strip()
    descripcion = (data.get('descripcion') or '').strip()
    fecha_str   = (data.get('fecha') or '').strip()
    hora_str    = (data.get('hora') or '').strip()
    lugar       = (data.get('lugar') or '').strip()
    categoria   = (data.get('categoria') or '').strip()
    status      = (data.get('status') or '').strip()

    # Solo actualizamos si viene algo
    if titulo:
        evento.title = titulo
    if descripcion:
        evento.description = descripcion
    if fecha_str:
        try:
            evento.date = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Fecha inválida. Use YYYY-MM-DD"}), 400
    if hora_str:
        try:
            evento.time = datetime.strptime(hora_str, "%H:%M").time()
        except ValueError:
            return jsonify({"error": "Hora inválida. Use HH:MM"}), 400
    if lugar:
        evento.location = lugar
    if categoria:
        evento.category = categoria
    if status:
        evento.status = status

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("[API] Error al actualizar evento:", repr(e))
        return jsonify({"error": "Error interno al actualizar evento"}), 500

    print(f"[API] Evento {event_id} actualizado por user_id={user_id}")
    return jsonify(evento.to_dict()), 200


@app.route('/api/mis-eventos', methods=['GET'])
def api_mis_eventos():
    """Obtiene eventos en los que está registrado el usuario (incluye QR)."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "No autenticado"}), 401

    # Unimos Registration con Event
    registros = (
        db.session.query(Registration, Event)
        .join(Event, Registration.event_id == Event.event_id)
        .filter(Registration.user_id == user_id)
        .order_by(Event.date, Event.time)
        .all()
    )

    payload = []
    for reg, ev in registros:
        payload.append({
            "registration_id": reg.registration_id,
            "qr_code": reg.qr_code,  # <- aquí viene la ruta tipo "qr/qr_reg_1.png"
            "evento_id": ev.event_id,
            "titulo": ev.title,
            "fecha": ev.date.isoformat() if ev.date else None,
            "hora": ev.time.strftime("%H:%M") if ev.time else None,
            "lugar": ev.location,
            "categoria": ev.category,
            "status_registro": reg.status
        })

    print(f"[API] GET /api/mis-eventos - {len(payload)} registros (user_id={user_id})")
    return jsonify(payload), 200



@app.route('/api/eventos/<int:evento_id>/registrar', methods=['POST'])
def api_registrar_evento(evento_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "No autenticado"}), 401

    # Verificar que el evento exista
    evento = Event.query.get(evento_id)
    if not evento:
        return jsonify({"error": "Evento no encontrado"}), 404

    # Verificar si ya está registrado
    ya_registrado = Registration.query.filter_by(
        user_id=user_id,
        event_id=evento_id
    ).first()

    if ya_registrado:
        # 👇 Opcional: si aún no tiene QR, lo generamos
        if not ya_registrado.qr_code:
            generar_qr_para_registro(ya_registrado)
            db.session.commit()

        return jsonify({
            "error": "Ya estás registrado en este evento",
            "registration_id": ya_registrado.registration_id,
            "qr_code": ya_registrado.qr_code
        }), 400

    # Crear nuevo registro
    registro = Registration(
        user_id=user_id,
        event_id=evento_id,
        status='inscrito'
    )
    db.session.add(registro)
    db.session.commit()  # aquí ya tiene registration_id

    # Generar QR para este registro
    generar_qr_para_registro(registro)
    db.session.commit()  # guardamos la ruta en registro.qr_code

    print(f"[REGISTRO] Usuario {user_id} registrado en evento {evento_id} "
          f"con registro {registro.registration_id}")

    return jsonify({
        "ok": True,
        "evento_id": evento_id,
        "registration_id": registro.registration_id,
        "qr_code": registro.qr_code
    }), 201




@app.route('/api/eventos/<int:evento_id>/desregistrar', methods=['POST'])
def api_desregistrar_evento(evento_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "No autenticado"}), 401

    registro = Registration.query.filter_by(
        user_id=user_id,
        event_id=evento_id
    ).first()

    if not registro:
        return jsonify({"error": "No estabas registrado en este evento"}), 400

    db.session.delete(registro)
    db.session.commit()

    print(f"[REGISTRO] Usuario {user_id} DESREGISTRADO de evento {evento_id}")
    return jsonify({"ok": True}), 200

@app.route('/eventos/<int:evento_id>/inscritos')
@require_roles(['admin'])
def ver_inscritos_evento(evento_id):
    """
    Muestra la lista de usuarios inscritos a un evento concreto.
    Usa la relación Registration.user -> User.
    """
    # 1. Verificar que haya sesión
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    # 2. Buscar el evento (404 si no existe)
    evento = Event.query.get_or_404(evento_id)

    # 3. Traer todos los registros de ese evento, con su usuario asociado
    #    Gracias a la relación Registration.user, luego podremos hacer reg.user
    from models import Registration, User  # si no los tienes ya importados arriba

    registros = (
        db.session.query(Registration)
        .join(Registration.user)                  # JOIN con la tabla users
        .filter(Registration.event_id == evento_id)
        .all()
    )

    # 4. Mandar todo al template
    return render_template(
        'inscritos_evento.html',
        evento=evento,
        registros=registros
    )



@app.route('/test_db')
def test_db():
    try:
        user = User.query.first()
        if user:
            # 👇 Usamos 'name' y 'email', que sí existen en tu tabla
            return f"Conexión OK. Primer usuario en BD: {user.name} ({user.email})"
        else:
            return "Conexión OK, pero no hay usuarios en la tabla 'users'."
    except Exception as e:
        return f"Error al conectar a la BD: {e}"


if __name__ == '__main__':
    app.run(debug=True)
