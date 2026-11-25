"""
Registro de todos los modelos del ORM (SQLAlchemy).
"""
from .administrador import Administrador
from .alumno import Alumno
from .contacto import MensajeContacto
from .personalidad import (
    ReactivoPersonalidad,
    RespuestaPersonalidad,
    ResultadoPersonalidad,
    TipoPersonalidad,
)
from .vark import OpcionVark, PreguntaVark, RespuestaVark, ResultadoVark

__all__ = [
    "Administrador",
    "Alumno",
    "MensajeContacto",
    "OpcionVark",
    "PreguntaVark",
    "ReactivoPersonalidad",
    "RespuestaPersonalidad",
    "RespuestaVark",
    "ResultadoPersonalidad",
    "ResultadoVark",
    "TipoPersonalidad",
]
