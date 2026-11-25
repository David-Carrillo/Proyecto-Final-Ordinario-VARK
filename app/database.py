"""
Conexión a la base de datos con el patrón de diseño SINGLETON.
Responsable: Gerardo

El patrón Singleton garantiza que en toda la aplicación exista UNA SOLA
instancia de la conexión (motor + fábrica de sesiones). No importa cuántas
veces se escriba BaseDatos(), siempre se obtiene el mismo objeto.

    >>> BaseDatos() is BaseDatos()
    True
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker


class Base(DeclarativeBase):
    """Clase base de la que heredan todos los modelos del ORM."""


class BaseDatos:
    """Administra la conexión a la base de datos (Singleton)."""

    _instancia = None

    def __new__(cls):
        # Si todavía no existe la instancia, se crea; si ya existe, se reutiliza.
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._iniciada = False
            cls._instancia.engine = None
            cls._instancia.sesion = None
        return cls._instancia

    def iniciar(self, url: str) -> None:
        """Crea el motor de SQLAlchemy una sola vez."""
        if self._iniciada:
            return
        argumentos = {"check_same_thread": False} if url.startswith("sqlite") else {}
        self.engine = create_engine(url, connect_args=argumentos)
        self.sesion = scoped_session(
            sessionmaker(bind=self.engine, expire_on_commit=False)
        )
        self._iniciada = True

    def crear_tablas(self) -> None:
        """Crea las tablas definidas en los modelos (si no existen)."""
        from app import models  # noqa: F401  (registra los modelos)

        Base.metadata.create_all(self.engine)

    def cerrar_sesion(self, _excepcion=None) -> None:
        """Libera la sesión al terminar cada petición HTTP."""
        if self.sesion is not None:
            self.sesion.remove()


# Instancia única que usa todo el proyecto
db = BaseDatos()
