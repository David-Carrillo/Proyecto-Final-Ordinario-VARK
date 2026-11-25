"""
Registro del cuestionario VARK en la base de datos.
Responsable: Lui
"""
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import db
from app.models import Alumno, OpcionVark, PreguntaVark, RespuestaVark, ResultadoVark
from app.services.calculos import CalculadoraVark, ErrorValidacion


class ServicioVark:
    def __init__(self):
        self.sesion = db.sesion

    def preguntas(self) -> list[PreguntaVark]:
        consulta = (
            select(PreguntaVark)
            .options(selectinload(PreguntaVark.opciones))
            .order_by(PreguntaVark.numero)
        )
        return list(self.sesion.scalars(consulta))

    def registrar(self, alumno: Alumno, ids_opciones: list) -> ResultadoVark:
        """Guarda las opciones elegidas y calcula el resultado."""
        try:
            ids = sorted({int(i) for i in ids_opciones})
        except (TypeError, ValueError):
            raise ErrorValidacion("Respuestas no válidas.")

        opciones = list(self.sesion.scalars(select(OpcionVark).where(OpcionVark.id.in_(ids))))
        if len(opciones) != len(ids):
            raise ErrorValidacion("Alguna de las respuestas no existe.")

        conteo, dominante = CalculadoraVark.calcular(o.estilo for o in opciones)

        resultado = ResultadoVark(
            alumno=alumno,
            visual=conteo["V"],
            auditivo=conteo["A"],
            lectura=conteo["R"],
            kinestesico=conteo["K"],
            estilo_dominante=dominante,
        )
        for opcion in opciones:
            resultado.respuestas.append(RespuestaVark(opcion=opcion))
        self.sesion.add(resultado)
        self.sesion.commit()
        return resultado

    def obtener(self, resultado_id: int):
        return self.sesion.get(ResultadoVark, resultado_id)

    def eliminar(self, resultado: ResultadoVark) -> None:
        self.sesion.delete(resultado)
        self.sesion.commit()
