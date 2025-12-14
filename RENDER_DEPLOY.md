# 🚀 Guía de Despliegue en Render

## Paso 1: Preparar el Repositorio

### 1.1 Hacer Push a GitHub
```bash
git add .
git commit -m "Preparación para despliegue en Render"
git push origin main
```

### 1.2 Verificar archivos incluidos
- ✅ `requirements.txt` - Dependencias actualizadas
- ✅ `Procfile` - Instrucciones de ejecución
- ✅ `render.yaml` - Configuración de Render
- ✅ `.env.example` - Variables de ejemplo
- ✅ `app.py` - Configurado con variables de entorno

## Paso 2: Crear Cuenta en Render

1. Ir a [render.com](https://render.com)
2. Registrarse con GitHub (recomendado)
3. Autorizar acceso a tus repositorios

## Paso 3: Desplegar la Aplicación

### Opción A: Usando render.yaml (RECOMENDADO)

1. En el dashboard de Render, click en **"New +"** → **"Blueprint"**
2. Conectar tu repositorio GitHub
3. Seleccionar el repositorio `quercus_project`
4. Click en **"Deploy"**
5. Render usará automáticamente `render.yaml`

### Opción B: Despliegue Manual

1. Click en **"New +"** → **"Web Service"**
2. Conectar repositorio GitHub
3. Configurar:
   - **Name**: `quercus-app`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (o Pro si necesitas)

4. Click en **"Create Web Service"**

## Paso 4: Crear Base de Datos PostgreSQL

1. En el dashboard de Render, click en **"New +"** → **"PostgreSQL"**
2. Configurar:
   - **Name**: `quercus-db`
   - **Database**: `quercus_db`
   - **User**: `postgres`
   - **Region**: (tu región más cercana)
   - **Plan**: Free

3. Click en **"Create Database"**

## Paso 5: Conectar la Base de Datos a la App

1. Copiar la **Internal Database URL** de la BD de Render
2. En tu Web Service, ir a **"Environment"**
3. Agregar variable:
   - **Key**: `DATABASE_URL`
   - **Value**: (pegar la Internal URL)

4. Agregar otra variable:
   - **Key**: `FLASK_SECRET_KEY`
   - **Value**: (generar una clave segura)

5. Click en **"Save"** → Render reiniciará automáticamente

## Paso 6: Inicializar la Base de Datos

### Opción A: Ejecutar Script SQL
```bash
# En Render Dashboard → PostgreSQL → Connect → psql
psql <your-connection-string> < quercus_db.sql
```

### Opción B: Usar Flask Migrate
```bash
# En la consola de Render o localmente:
flask db upgrade
```

## Paso 7: Verificar el Despliegue

1. Ir a la URL de tu aplicación (algo como `https://quercus-app.onrender.com`)
2. Verificar que carga la página
3. Probar login con credenciales

## Variables de Entorno Necesarias

```
DATABASE_URL        → Conexión a PostgreSQL de Render
FLASK_ENV          → production
FLASK_SECRET_KEY   → Clave segura para sesiones
PORT               → (Render lo asigna automáticamente)
```

## Troubleshooting

### La app no inicia
```
Ver logs: Dashboard → Web Service → Logs
Verificar que DATABASE_URL esté correcta
Revisar que PORT esté configurado correctamente
```

### Error de BD
```
Verificar que PostgreSQL esté creado
Confirmar que DATABASE_URL esté configurada
Ejecutar flask db upgrade
```

### Errores de dependencias
```
Verificar requirements.txt está en la raíz del proyecto
Asegurar que gunicorn esté incluido
```

## Deploy Automático

Render desplegará automáticamente cada vez que hagas push a la rama `main`:

```bash
git add .
git commit -m "Tu mensaje"
git push origin main
# Render detectará automáticamente y hará deploy
```

## Monitoreo en Producción

1. Ver logs en tiempo real: Dashboard → Logs
2. Verificar uso de recursos: Dashboard → Metrics
3. Reiniciar si es necesario: Dashboard → Restart

## Configuración Recomendada para Producción

```python
# En app.py (ya configurado)
FLASK_ENV = production
DEBUG = False
SQLALCHEMY_ECHO = False  # No loguear queries
```

## URLs Útiles

- Dashboard Render: https://dashboard.render.com
- Documentación: https://render.com/docs
- Estado: https://status.render.com

---

**¿Necesitas ayuda?** Revisa los logs en el dashboard de Render para diagnosticar problemas.
