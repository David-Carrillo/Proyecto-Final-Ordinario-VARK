"""
Registro del test de personalidad en la base de datos.
Responsable: Lui
"""
from sqlalchemy import select

from app.database import db
from app.models import (
    Alumno,
    ReactivoPersonalidad,
    RespuestaPersonalidad,
    ResultadoPersonalidad,
    TipoPersonalidad,
)
from app.services.calculos import CalculadoraPersonalidad, ErrorValidacion


class ServicioPersonalidad:
    def __init__(self):
        self.sesion = db.sesion

    def reactivos_por_dimension(self) -> dict[int, list[ReactivoPersonalidad]]:
        consulta = select(ReactivoPersonalidad).order_by(
            ReactivoPersonalidad.dimension, ReactivoPersonalidad.orden
        )
        agrupados: dict[int, list] = {}
        for reactivo in self.sesion.scalars(consulta):
            agrupados.setdefault(reactivo.dimension, []).append(reactivo)
        return agrupados

    def registrar(self, alumno: Alumno, puntos: dict) -> ResultadoPersonalidad:
        """
        puntos = {reactivo_id: (puntos_a, puntos_b)}
        Todos los reactivos son obligatorios.
        """
        reactivos = list(self.sesion.scalars(select(ReactivoPersonalidad)))
        faltan = [r for r in reactivos if r.id not in puntos]
        if faltan:
            raise ErrorValidacion(f"Faltan {len(faltan)} renglones por contestar.")

        filas = []
        for r in reactivos:
            a, b = puntos[r.id]
            filas.append((r.letra_a, a, r.letra_b, b))
        totales, tipo = CalculadoraPersonalidad.calcular(filas)

        resultado = ResultadoPersonalidad(
            alumno=alumno,
            e=totales["E"], i=totales["I"],
            s=totales["S"], n=totales["N"],
            t=totales["T"], f=totales["F"],
            j=totales["J"], p=totales["P"],
            tipo=self.sesion.get(TipoPersonalidad, tipo),
        )
        for r in reactivos:
            a, b = puntos[r.id]
            resultado.respuestas.append(
                RespuestaPersonalidad(reactivo=r, puntos_a=int(a), puntos_b=int(b))
            )
        self.sesion.add(resultado)
        self.sesion.commit()
        return resultado

    def obtener(self, resultado_id: int):
        return self.sesion.get(ResultadoPersonalidad, resultado_id)

    def tipos(self) -> list[TipoPersonalidad]:
        return list(self.sesion.scalars(select(TipoPersonalidad).order_by(TipoPersonalidad.numero)))

    def tipo(self, codigo: str):
        return self.sesion.get(TipoPersonalidad, codigo.upper())

    def eliminar(self, resultado: ResultadoPersonalidad) -> None:
        self.sesion.delete(resultado)
        self.sesion.commit()
