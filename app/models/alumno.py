"""
Modelo Alumno.
Responsable: Lui
"""
from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Alumno(Base):
    __tablename__ = "alumnos"

    id: Mapped[int] = mapped_column(primary_key=True)
    matricula: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120))
    carrera: Mapped[str] = mapped_column(String(100), index=True)
    semestre: Mapped[int] = mapped_column(Integer, index=True)
    grupo: Mapped[str] = mapped_column(String(20), index=True)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    resultados_vark: Mapped[list["ResultadoVark"]] = relationship(
        back_populates="alumno",
        cascade="all, delete-orphan",
        order_by="ResultadoVark.fecha.desc()",
    )
    resultados_personalidad: Mapped[list["ResultadoPersonalidad"]] = relationship(
        back_populates="alumno",
        cascade="all, delete-orphan",
        order_by="ResultadoPersonalidad.fecha.desc()",
    )

    @property
    def ultimo_vark(self):
        return self.resultados_vark[0] if self.resultados_vark else None

    @property
    def ultima_personalidad(self):
        return self.resultados_personalidad[0] if self.resultados_personalidad else None

    def to_dict(self) -> dict:
        return {
            "matricula": self.matricula,
            "nombre": self.nombre,
            "carrera": self.carrera,
            "semestre": self.semestre,
            "grupo": self.grupo,
            "vark": self.ultimo_vark.to_dict() if self.ultimo_vark else None,
            "personalidad": (
                self.ultima_personalidad.to_dict() if self.ultima_personalidad else None
            ),
        }

    def __repr__(self) -> str:
        return f"<Alumno {self.matricula} {self.nombre}>"
