# AUTOGEN_EVENTS_START
eventos = [
    {'id': 1, 'titulo': 'Charla de Ingeniería de Software', 'descripcion': 'Introducción a metodologías ágiles', 'fecha': '2025-12-01'},
    {'id': 2, 'titulo': 'Workshop Python', 'descripcion': 'Aprende Python desde cero', 'fecha': '2025-12-05'},
    {'id': 3, 'titulo': 'Hackathon UNAL', 'descripcion': 'Competencia de programación', 'fecha': '2025-12-10'}
]
# AUTOGEN_EVENTS_END

# AUTOGEN_REGISTROS_START
registros = []
# AUTOGEN_REGISTROS_END

def get_events():
    return eventos

def get_registros():
    """Obtiene todos los registros usuario-evento."""
    return registros

def add_event(titulo, descripcion, fecha):
    """
    Añade un evento en memoria y persiste en este mismo archivo (bloque AUTOGEN).
    """
    next_id = 1
    if eventos:
        next_id = max(e.get("id", 0) for e in eventos) + 1
    evento = {"id": next_id, "titulo": titulo, "descripcion": descripcion, "fecha": fecha}
    eventos.append(evento)
    _persist_autogen()
    return evento

def registrar_usuario_evento(usuario, evento_id):
    """Registra un usuario en un evento."""
    # Evitar duplicados
    if any(r.get('usuario') == usuario and r.get('evento_id') == evento_id for r in registros):
        print(f"[WARN] {usuario} ya está registrado en evento {evento_id}")
        return False
    
    registro = {
        'usuario': usuario,
        'evento_id': evento_id
    }
    
    registros.append(registro)
    _persist_autogen()
    print(f"[INFO] {usuario} registrado en evento {evento_id}")
    return True

def obtener_eventos_usuario(usuario):
    """Retorna lista de eventos en los que está registrado un usuario."""
    evento_ids = [r.get('evento_id') for r in registros if r.get('usuario') == usuario]
    mis_eventos = [e for e in eventos if e.get('id') in evento_ids]
    return mis_eventos

def desregistrar_usuario(usuario, evento_id):
    """Desregistra un usuario de un evento."""
    global registros
    nuevos = [r for r in registros if not (r.get('usuario') == usuario and r.get('evento_id') == evento_id)]
    
    if len(nuevos) < len(registros):
        registros = nuevos
        _persist_autogen()
        print(f"[INFO] {usuario} desregistrado de evento {evento_id}")
        return True
    return False

def usuario_registrado_en_evento(usuario, evento_id):
    """Verifica si un usuario está registrado en un evento."""
    return any(r.get('usuario') == usuario and r.get('evento_id') == evento_id for r in registros)

def _persist_autogen():
    import io, os, pprint
    path = os.path.abspath(__file__)
    with io.open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Guardar eventos
    start_ev = content.find('# AUTOGEN_EVENTS_START')
    end_ev = content.find('# AUTOGEN_EVENTS_END')
    
    # Guardar registros
    start_reg = content.find('# AUTOGEN_REGISTROS_START')
    end_reg = content.find('# AUTOGEN_REGISTROS_END')
    
    if start_ev == -1 or end_ev == -1 or start_reg == -1 or end_reg == -1:
        print("[ERROR] Marcadores AUTOGEN no encontrados")
        return
    
    # Construir nuevo contenido
    before_ev = content[:start_ev]
    between = content[end_ev + len('# AUTOGEN_EVENTS_END') : start_reg]
    after_reg = content[end_reg + len('# AUTOGEN_REGISTROS_END') :]
    
    events_repr = pprint.pformat(eventos, width=120, sort_dicts=True)
    registros_repr = pprint.pformat(registros, width=120, sort_dicts=True)
    
    new_block_ev = '# AUTOGEN_EVENTS_START\nevento = ' + events_repr + '\n# AUTOGEN_EVENTS_END'
    new_block_reg = '# AUTOGEN_REGISTROS_START\nregistros = ' + registros_repr + '\n# AUTOGEN_REGISTROS_END'
    
    new_content = before_ev + new_block_ev + between + new_block_reg + after_reg
    
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)