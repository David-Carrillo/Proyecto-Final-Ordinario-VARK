"""
Modelos del test de personalidad (tipología de Jung y Myers-Briggs).
Responsable: Lui

ReactivoPersonalidad   cada renglón del test: par de frases (columna A y C)
TipoPersonalidad       los 16 tipos con peligros y sugerencias
ResultadoPersonalidad  1 ── N  RespuestaPersonalidad
"""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ReactivoPersonalidad(Base):
    __tablename__ = "personalidad_reactivos"

    id: Mapped[int] = mapped_column(primary_key=True)
    dimension: Mapped[int] = mapped_column(Integer, index=True)  # 1 a 4
    orden: Mapped[int] = mapped_column(Integer)
    texto_a: Mapped[str] = mapped_column(String(150))
    letra_a: Mapped[str] = mapped_column(String(1))  # E, S, T, J
    texto_b: Mapped[str] = mapped_column(String(150))
    letra_b: Mapped[str] = mapped_column(String(1))  # I, N, F, P


class TipoPersonalidad(Base):
    __tablename__ = "personalidad_tipos"

    codigo: Mapped[str] = mapped_column(String(4), primary_key=True)  # ej. ISTJ
    numero: Mapped[int] = mapped_column(Integer)
    temperamento: Mapped[str] = mapped_column(String(40))
    peligros: Mapped[str] = mapped_column(Text)      # un renglón por punto
    sugerencias: Mapped[str] = mapped_column(Text)   # un renglón por punto

    @property
    def lista_peligros(self) -> list[str]:
        return [p for p in self.peligros.splitlines() if p.strip()]

    @property
    def lista_sugerencias(self) -> list[str]:
        return [s for s in self.sugerencias.splitlines() if s.strip()]


class ResultadoPersonalidad(Base):
    __tablename__ = "personalidad_resultados"

    id: Mapped[int] = mapped_column(primary_key=True)
    alumno_id: Mapped[int] = mapped_column(ForeignKey("alumnos.id"), index=True)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    e: Mapped[int] = mapped_column(Integer)
    i: Mapped[int] = mapped_column(Integer)
    s: Mapped[int] = mapped_column(Integer)
    n: Mapped[int] = mapped_column(Integer)
    t: Mapped[int] = mapped_column(Integer)
    f: Mapped[int] = mapped_column(Integer)
    j: Mapped[int] = mapped_column(Integer)
    p: Mapped[int] = mapped_column(Integer)
    tipo_codigo: Mapped[str] = mapped_column(ForeignKey("personalidad_tipos.codigo"))

    alumno: Mapped["Alumno"] = relationship(back_populates="resultados_personalidad")
    tipo: Mapped["TipoPersonalidad"] = relationship()
    respuestas: Mapped[list["RespuestaPersonalidad"]] = relationship(
        back_populates="resultado", cascade="all, delete-orphan"
    )

    @property
    def totales(self) -> dict:
        return {
            "E": self.e, "I": self.i, "S": self.s, "N": self.n,
            "T": self.t, "F": self.f, "J": self.j, "P": self.p,
        }

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "fecha": self.fecha.strftime("%Y-%m-%d %H:%M"),
            "totales": self.totales,
            "tipo": self.tipo_codigo,
            "temperamento": self.tipo.temperamento if self.tipo else None,
        }


class RespuestaPersonalidad(Base):
    __tablename__ = "personalidad_respuestas"

    id: Mapped[int] = mapped_column(primary_key=True)
    resultado_id: Mapped[int] = mapped_column(ForeignKey("personalidad_resultados.id"))
    reactivo_id: Mapped[int] = mapped_column(ForeignKey("personalidad_reactivos.id"))
    puntos_a: Mapped[int] = mapped_column(Integer)
    puntos_b: Mapped[int] = mapped_column(Integer)

    resultado: Mapped["ResultadoPersonalidad"] = relationship(back_populates="respuestas")
    reactivo: Mapped["ReactivoPersonalidad"] = relationship()
