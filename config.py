"""
Configuración general de la aplicación.
Responsable: Gerardo

Todos los valores se pueden cambiar con variables de entorno, así no se
sube ninguna contraseña al repositorio.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Clave para firmar las sesiones (cámbiala en producción)
    SECRET_KEY = os.environ.get("SECRET_KEY", "cambia-esta-clave-secreta")

    # Base de datos: SQLite por defecto. Para MySQL bastaría con:
    # DATABASE_URL=mysql+pymysql://usuario:password@localhost/vark
    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "vark.db"),
    )

    # Correo para el formulario de contacto (Gmail con "contraseña de aplicación")
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DESTINO = os.environ.get("MAIL_DESTINO", "")

    # Administrador que se crea la primera vez que corre el sistema
    ADMIN_USUARIO = os.environ.get("ADMIN_USUARIO", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
