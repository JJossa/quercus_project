# users.py
# Este módulo sirve como "base de datos" temporal
# Más adelante lo conectaremos a SQLite

# AUTOGEN_USERS_START
usuarios = {'admin': {'contrasena': 'admin', 'correo': 'admin'}, 'daniel': {'contrasena': '123', 'correo': 'daniel@unal.edu.co'}}
# AUTOGEN_USERS_END

def get_users():
    return usuarios

def add_user(usuario, correo, contrasena):
    """
    Añade un usuario en memoria y persiste el bloque AUTOGEN en este mismo archivo.
    Uso temporal para la primera entrega.
    """
    usuarios[usuario] = {"correo": correo, "contrasena": contrasena}
    _persist_autogen()

def _persist_autogen():
    import io, os, pprint
    path = os.path.abspath(__file__)
    with io.open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    start = content.find('# AUTOGEN_USERS_START')
    end = content.find('# AUTOGEN_USERS_END')
    if start == -1 or end == -1:
        # no se encontró el bloque; no sobrescribimos
        return
    before = content[:start]
    after = content[end + len('# AUTOGEN_USERS_END') :]
    # construir representación legible del dict
    users_repr = pprint.pformat(usuarios, width=120, sort_dicts=True)
    new_block = '# AUTOGEN_USERS_START\n' + 'usuarios = ' + users_repr + '\n# AUTOGEN_USERS_END'
    new_content = before + new_block + after
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
