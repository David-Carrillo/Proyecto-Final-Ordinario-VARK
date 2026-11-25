"""
Carga inicial de datos: preguntas VARK, reactivos y tipos de personalidad,
y el primer administrador.
Responsable: Lui

Solo inserta los datos si las tablas están vacías, así que se puede
ejecutar cada vez que arranca la aplicación sin duplicar nada.
"""
from sqlalchemy import func, select

from app.data.carreras import normalizar_carrera
from app.data.instrumentos import (
    PREGUNTAS_VARK,
    REACTIVOS_PERSONALIDAD,
    TIPOS_PERSONALIDAD,
    estilo_de_opcion,
)
from app.database import db
from app.models import (
    Administrador,
    Alumno,
    OpcionVark,
    PreguntaVark,
    ReactivoPersonalidad,
    TipoPersonalidad,
)
from app.services.calculos import DIMENSIONES, CalculadoraPersonalidad


class CargadorDatos:
    def __init__(self):
        self.sesion = db.sesion

    def _vacia(self, modelo) -> bool:
        return self.sesion.scalar(select(func.count()).select_from(modelo)) == 0

    def cargar_vark(self) -> None:
        if not self._vacia(PreguntaVark):
            return
        for numero, texto, opciones in PREGUNTAS_VARK:
            pregunta = PreguntaVark(numero=numero, texto=texto)
            for letra, texto_opcion in opciones:
                pregunta.opciones.append(
                    OpcionVark(
                        letra=letra,
                        texto=texto_opcion,
                        estilo=estilo_de_opcion(numero, letra),
                    )
                )
            self.sesion.add(pregunta)

    def cargar_personalidad(self) -> None:
        if self._vacia(ReactivoPersonalidad):
            for dimension, renglones in REACTIVOS_PERSONALIDAD.items():
                letra_a, letra_b, _nombre = DIMENSIONES[dimension]
                for orden, (texto_a, texto_b) in enumerate(renglones, start=1):
                    self.sesion.add(
                        ReactivoPersonalidad(
                            dimension=dimension,
                            orden=orden,
                            texto_a=texto_a,
                            letra_a=letra_a,
                            texto_b=texto_b,
                            letra_b=letra_b,
                        )
                    )
        if self._vacia(TipoPersonalidad):
            for numero, codigo, peligros, sugerencias in TIPOS_PERSONALIDAD:
                self.sesion.add(
                    TipoPersonalidad(
                        codigo=codigo,
                        numero=numero,
                        temperamento=CalculadoraPersonalidad.temperamento(codigo)["nombre"],
                        peligros="\n".join(peligros),
                        sugerencias="\n".join(sugerencias),
                    )
                )

    def crear_admin_inicial(self, usuario: str, password: str) -> None:
        if not self._vacia(Administrador):
            return
        admin = Administrador(usuario=usuario, nombre="Administrador", email="")
        admin.establecer_password(password)
        self.sesion.add(admin)

    def normalizar_carreras(self) -> None:
        """Corrige carreras guardadas con siglas o escritas de otra forma."""
        for alumno in self.sesion.scalars(select(Alumno)):
            oficial = normalizar_carrera(alumno.carrera)
            if oficial and oficial != alumno.carrera:
                alumno.carrera = oficial

    def ejecutar(self, usuario_admin: str, password_admin: str) -> None:
        self.normalizar_carreras()
        self.cargar_vark()
        self.cargar_personalidad()
        self.crear_admin_inicial(usuario_admin, password_admin)
        self.sesion.commit()
