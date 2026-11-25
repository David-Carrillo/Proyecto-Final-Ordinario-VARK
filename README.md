# Aprendizaje VARK y Test de Personalidad

Aplicación web en **Python (Flask)** para aplicar y analizar el cuestionario de estilos de aprendizaje **VARK** y el test de personalidad basado en la tipología de **Jung y Myers-Briggs**.

Equipo: **Gerardo**, **Lui** y **Valeria**.

## Cómo correrlo (Windows, Mac o Linux)

Se necesita Python 3.10 o más nuevo.

```bash
# 1. Entrar a la carpeta del proyecto
cd vark_personalidad

# 2. Crear y activar un entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. (Opcional) Cargar 30 alumnos de prueba y los 2 ejemplos de los PDF
python datos_prueba.py

# 5. Arrancar
python run.py
```

Abrir **http://127.0.0.1:5000**

- Administrador inicial: usuario **admin**, contraseña **admin123** (cámbienla en *Admin → Administradores*).
- La base de datos SQLite se crea sola en `instance/vark.db` con las preguntas ya cargadas.
- Pruebas automáticas: `python -m unittest discover -s tests -v`

### Correo del formulario de contacto (opcional)

Si no se configura, los mensajes se guardan y se leen en *Admin → Mensajes*. Para enviarlos por Gmail, crea una *contraseña de aplicación* y define antes de `python run.py`:

```bash
set MAIL_USERNAME=tucorreo@gmail.com      # Windows (en Mac/Linux usa export)
set MAIL_PASSWORD=contraseña_de_aplicacion
set MAIL_DESTINO=tucorreo@gmail.com
```

## Estructura de carpetas

```
vark_personalidad/
├── run.py                  Punto de entrada
├── config.py               Configuración (BD, correo, admin inicial)
├── datos_prueba.py         Carga alumnos de prueba
├── requirements.txt
├── app/
│   ├── __init__.py         Fábrica de la app (create_app)
│   ├── database.py         Conexión a BD con patrón SINGLETON
│   ├── models/             Modelos ORM (SQLAlchemy)
│   ├── services/           Lógica de negocio (cálculos, estadísticas, PDF, correo)
│   ├── routes/             Controladores: público, instrumentos, auth, admin, API REST
│   ├── data/               Contenido de los instrumentos y carga inicial
│   ├── templates/          Vistas HTML (Jinja2 + Bootstrap 5)
│   └── static/             CSS, JS (jQuery, Chart.js), imágenes, video y audio
└── tests/                  Pruebas unitarias
```

## Quién hizo qué

| Integrante | Archivos principales |
|---|---|
| **Gerardo** (backend) | `config.py`, `run.py`, `app/__init__.py`, `database.py` (Singleton), `routes/auth.py`, `routes/admin.py` (mantenimiento), `routes/api.py`, `routes/publico.py`, `services/correo_service.py`, `models/administrador.py`, `models/contacto.py`, `datos_prueba.py`, video y audio |
| **Lui** (datos y cálculos) | `models/alumno.py`, `models/vark.py`, `models/personalidad.py`, `data/`, `services/calculos.py`, `services/vark_service.py`, `services/personalidad_service.py`, `services/alumno_service.py` (búsqueda), `services/estadisticas_service.py`, `services/reporte_pdf.py`, `tests/` |
| **Valeria** (frontend) | `templates/`, `static/css/estilos.css`, `static/js/` (validaciones jQuery y gráficas), imágenes optimizadas del PSD |

## Requisitos del profesor y dónde se cumplen

| Requisito | Dónde |
|---|---|
| Sitio web profesional | Diseño basado en `Consulting.psd` (`templates/base.html`, `estilos.css`) |
| Formulario y BD VARK | `/vark`, `models/vark.py` |
| VARK individual, grupal o total | Filtro de ámbito en *Admin → Resultados y gráficas* |
| Cálculo VARK con gráficas y dashboard | `/vark/resultado/<id>`, `/admin/dashboard` |
| Formulario de personalidad | `/personalidad` |
| Personalidad individual o grupal | Enlaces grupales en *Admin → Panel*; filtro de ámbito |
| Resultado de personalidad con dashboard | `/personalidad/resultado/<id>`, `/admin/dashboard` |
| Búsqueda por alumno, grupo o total | `/admin/dashboard`, `/admin/alumnos`, `/consultar` |
| Mantenimiento (altas, bajas, cambios) solo admin | *Admin → Alumnos, Administradores, Tipos, Mensajes* |
| Autenticación de administradores (zona pública y privada) | `routes/auth.py` |
| Formulario de contacto por correo | `/contacto` |
| Responsivo | Bootstrap 5 + media queries |
| Video de 2 a 4 minutos | `/acerca` (`static/media/video/presentacion.mp4`) |
| Búsqueda y PDF con ficha técnica | `/admin/reporte.pdf`, `/consultar/<matricula>/pdf` |
| Dashboard con gráfica para resultados grupales | `/admin/dashboard` |
| Base de datos | SQLite (`instance/vark.db`), cambiable a MySQL en `config.py` |
| ORM | SQLAlchemy 2 (`app/models/`) |
| Patrón Singleton | `app/database.py` |
| API REST | `/api/v1/...` (`routes/api.py`) |
| POO, sin PHP | Clases en modelos, servicios y conexión; todo en Python |
| Photoshop (optimización) | `static/img/hero-decoracion.jpg` recortado y comprimido del PSD |
| Audio | `/acerca` (`static/media/audio/bienvenida.mp3`) |

## API REST

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/estadisticas?ambito=total` | Resumen VARK y personalidad (`ambito`: total, grupal, individual; filtros `carrera`, `semestre`, `grupo`, `matricula`) |
| GET | `/api/v1/alumnos` | Alumnos con su último resultado (requiere sesión de admin) |
| GET | `/api/v1/alumnos/<matricula>` | Un alumno (requiere sesión de admin) |
| GET | `/api/v1/tipos` | Los 16 tipos de personalidad |
| GET | `/api/v1/vark/preguntas` | Preguntas del cuestionario VARK |

## Publicar en internet (Render, gratis)

1. Subir el proyecto a GitHub.
2. En render.com: *New → Web Service* y elegir el repositorio.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn "app:create_app()"`
5. Variables de entorno: `SECRET_KEY`, `ADMIN_PASSWORD` y, si se quiere correo, `MAIL_*`.

En el plan gratis de Render el disco se borra al reiniciar. Para la presentación sirve, pero para guardar datos permanentes usen una base de datos externa (`DATABASE_URL`) o PythonAnywhere.
