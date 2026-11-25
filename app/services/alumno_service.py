"""
Operaciones con alumnos y búsqueda por alumno, grupo o total.
Responsable: Lui
"""
from dataclasses import dataclass

from sqlalchemy import select

from app.data.carreras import OPCION_OTRA, normalizar_carrera
from app.database import db
from app.models import Alumno
from app.services.calculos import ErrorValidacion


@dataclass
class Filtro:
    """
    Ámbito de una búsqueda:
      - individual: un alumno por matrícula
      - grupal: por carrera, semestre y/o grupo
      - total: todos los alumnos
    """

    ambito: str = "total"
    matricula: str = ""
    nombre: str = ""
    carrera: str = ""
    semestre: str = ""
    grupo: str = ""

    @classmethod
    def desde_peticion(cls, args) -> "Filtro":
        ambito = args.get("ambito", "total")
        if ambito not in ("individual", "grupal", "total"):
            ambito = "total"
        return cls(
            ambito=ambito,
            matricula=args.get("matricula", "").strip(),
            nombre=args.get("nombre", "").strip(),
            carrera=args.get("carrera", "").strip(),
            semestre=args.get("semestre", "").strip(),
            grupo=args.get("grupo", "").strip(),
        )

    def como_dict(self) -> dict:
        return {
            "ambito": self.ambito,
            "matricula": self.matricula,
            "nombre": self.nombre,
            "carrera": self.carrera,
            "semestre": self.semestre,
            "grupo": self.grupo,
        }

    @property
    def titulo(self) -> str:
        if self.ambito == "individual":
            return f"Alumno {self.matricula or self.nombre}"
        if self.ambito == "grupal":
            partes = []
            if self.carrera:
                partes.append(self.carrera)
            if self.semestre:
                partes.append(f"{self.semestre}° semestre")
            if self.grupo:
                partes.append(f"grupo {self.grupo}")
            return "Grupo: " + (", ".join(partes) if partes else "todos")
        return "Total de alumnos"


class ServicioAlumnos:
    def __init__(self):
        self.sesion = db.sesion

    @staticmethod
    def validar_datos(datos) -> dict:
        # La carrera viene de la lista desplegable; si eligieron "Otra",
        # se toma lo que escribieron y se intenta llevar al nombre oficial.
        carrera = datos.get("carrera", "")
        if carrera == OPCION_OTRA:
            carrera = datos.get("carrera_otra", "")
        limpio = {
            "matricula": datos.get("matricula", "").strip().upper(),
            "nombre": " ".join(datos.get("nombre", "").split()),
            "carrera": normalizar_carrera(carrera),
            "semestre": datos.get("semestre", "").strip(),
            "grupo": datos.get("grupo", "").strip().upper(),
        }
        faltantes = [campo for campo, valor in limpio.items() if not valor]
        if faltantes:
            raise ErrorValidacion("Faltan datos del alumno: " + ", ".join(faltantes))
        if not limpio["semestre"].isdigit() or not 1 <= int(limpio["semestre"]) <= 12:
            raise ErrorValidacion("El semestre debe ser un número del 1 al 12.")
        limpio["semestre"] = int(limpio["semestre"])
        return limpio

    def por_matricula(self, matricula: str):
        return self.sesion.scalar(
            select(Alumno).where(Alumno.matricula == matricula.strip().upper())
        )

    def por_id(self, alumno_id: int):
        return self.sesion.get(Alumno, alumno_id)

    def registrar_o_actualizar(self, datos) -> Alumno:
        """Si la matrícula ya existe se actualizan sus datos; si no, se crea."""
        limpio = self.validar_datos(datos)
        alumno = self.por_matricula(limpio["matricula"])
        if alumno is None:
            alumno = Alumno(**limpio)
            self.sesion.add(alumno)
        else:
            for campo, valor in limpio.items():
                setattr(alumno, campo, valor)
        self.sesion.flush()
        return alumno

    def eliminar(self, alumno: Alumno) -> None:
        self.sesion.delete(alumno)
        self.sesion.commit()

    def buscar(self, filtro: Filtro) -> list[Alumno]:
        consulta = select(Alumno)
        if filtro.ambito == "individual":
            if filtro.matricula:
                consulta = consulta.where(Alumno.matricula == filtro.matricula.upper())
            elif filtro.nombre:
                consulta = consulta.where(Alumno.nombre.ilike(f"%{filtro.nombre}%"))
            else:
                return []
        elif filtro.ambito == "grupal":
            if filtro.carrera:
                consulta = consulta.where(Alumno.carrera.ilike(f"%{filtro.carrera}%"))
            if filtro.semestre.isdigit():
                consulta = consulta.where(Alumno.semestre == int(filtro.semestre))
            if filtro.grupo:
                consulta = consulta.where(Alumno.grupo == filtro.grupo.upper())
        consulta = consulta.order_by(Alumno.carrera, Alumno.semestre, Alumno.grupo, Alumno.nombre)
        return list(self.sesion.scalars(consulta))

    def valores_distintos(self) -> dict:
        """Listas de carreras, semestres y grupos registrados (para los filtros)."""
        def distintos(columna):
            return [v for v in self.sesion.scalars(select(columna).distinct().order_by(columna)) if v]

        return {
            "carreras": distintos(Alumno.carrera),
            "semestres": distintos(Alumno.semestre),
            "grupos": distintos(Alumno.grupo),
        }
