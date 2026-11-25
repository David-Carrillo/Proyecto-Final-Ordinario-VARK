"""
Modelos del instrumento VARK.
Responsable: Lui

PreguntaVark   1 ── N  OpcionVark        (cada pregunta tiene 4 opciones a, b, c, d)
ResultadoVark  1 ── N  RespuestaVark     (opciones que eligió el alumno)
"""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.services.calculos import CalculadoraVark


class PreguntaVark(Base):
    __tablename__ = "vark_preguntas"

    id: Mapped[int] = mapped_column(primary_key=True)
    numero: Mapped[int] = mapped_column(Integer, unique=True)
    texto: Mapped[str] = mapped_column(Text)

    opciones: Mapped[list["OpcionVark"]] = relationship(
        back_populates="pregunta",
        cascade="all, delete-orphan",
        order_by="OpcionVark.letra",
    )


class OpcionVark(Base):
    __tablename__ = "vark_opciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    pregunta_id: Mapped[int] = mapped_column(ForeignKey("vark_preguntas.id"))
    letra: Mapped[str] = mapped_column(String(1))   # a, b, c, d
    texto: Mapped[str] = mapped_column(Text)
    estilo: Mapped[str] = mapped_column(String(1))  # V, A, R, K

    pregunta: Mapped["PreguntaVark"] = relationship(back_populates="opciones")


class ResultadoVark(Base):
    __tablename__ = "vark_resultados"

    id: Mapped[int] = mapped_column(primary_key=True)
    alumno_id: Mapped[int] = mapped_column(ForeignKey("alumnos.id"), index=True)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    visual: Mapped[int] = mapped_column(Integer, default=0)
    auditivo: Mapped[int] = mapped_column(Integer, default=0)
    lectura: Mapped[int] = mapped_column(Integer, default=0)
    kinestesico: Mapped[int] = mapped_column(Integer, default=0)
    estilo_dominante: Mapped[str] = mapped_column(String(4))  # ej. "V" o "VK"

    alumno: Mapped["Alumno"] = relationship(back_populates="resultados_vark")
    respuestas: Mapped[list["RespuestaVark"]] = relationship(
        back_populates="resultado", cascade="all, delete-orphan"
    )

    @property
    def conteo(self) -> dict:
        return {
            "V": self.visual,
            "A": self.auditivo,
            "R": self.lectura,
            "K": self.kinestesico,
        }

    @property
    def descripcion(self) -> str:
        return CalculadoraVark.describir(self.estilo_dominante)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "fecha": self.fecha.strftime("%Y-%m-%d %H:%M"),
            "conteo": self.conteo,
            "estilo_dominante": self.estilo_dominante,
            "descripcion": self.descripcion,
        }


class RespuestaVark(Base):
    __tablename__ = "vark_respuestas"

    id: Mapped[int] = mapped_column(primary_key=True)
    resultado_id: Mapped[int] = mapped_column(ForeignKey("vark_resultados.id"))
    opcion_id: Mapped[int] = mapped_column(ForeignKey("vark_opciones.id"))

    resultado: Mapped["ResultadoVark"] = relationship(back_populates="respuestas")
    opcion: Mapped["OpcionVark"] = relationship()
