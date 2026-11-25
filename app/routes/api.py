"""
API REST (JSON).
Responsable: Gerardo

Endpoints:
  GET /api/v1/estadisticas?ambito=total|grupal|individual&carrera=&semestre=&grupo=&matricula=
      Resumen VARK y de personalidad (lo usan las gráficas del dashboard).
  GET /api/v1/alumnos?ambito=...            Lista de alumnos con su último resultado (solo admin)
  GET /api/v1/alumnos/<matricula>           Un alumno con su último resultado (solo admin)
  GET /api/v1/tipos                         Los 16 tipos de personalidad
  GET /api/v1/vark/preguntas                Preguntas del cuestionario VARK
"""
from flask import Blueprint, jsonify, request

from app.routes.auth import admin_actual
from app.services.alumno_service import Filtro, ServicioAlumnos
from app.services.estadisticas_service import Estadisticas
from app.services.personalidad_service import ServicioPersonalidad
from app.services.vark_service import ServicioVark

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


def _error(mensaje: str, codigo: int):
    return jsonify({"ok": False, "error": mensaje}), codigo


@api_bp.get("/estadisticas")
def estadisticas():
    filtro = Filtro.desde_peticion(request.args)
    if filtro.ambito == "individual" and admin_actual() is None:
        return _error("Se requiere iniciar sesión como administrador.", 401)
    alumnos = ServicioAlumnos().buscar(filtro)
    return jsonify({"ok": True, "filtro": filtro.como_dict(), "titulo": filtro.titulo,
                    "datos": Estadisticas(alumnos).resumen()})


@api_bp.get("/alumnos")
def alumnos():
    if admin_actual() is None:
        return _error("Se requiere iniciar sesión como administrador.", 401)
    filtro = Filtro.desde_peticion(request.args)
    lista = ServicioAlumnos().buscar(filtro)
    return jsonify({"ok": True, "total": len(lista), "alumnos": [a.to_dict() for a in lista]})


@api_bp.get("/alumnos/<matricula>")
def alumno(matricula):
    if admin_actual() is None:
        return _error("Se requiere iniciar sesión como administrador.", 401)
    encontrado = ServicioAlumnos().por_matricula(matricula)
    if encontrado is None:
        return _error("Alumno no encontrado.", 404)
    return jsonify({"ok": True, "alumno": encontrado.to_dict()})


@api_bp.get("/tipos")
def tipos():
    return jsonify({"ok": True, "tipos": [
        {"codigo": t.codigo, "temperamento": t.temperamento,
         "peligros": t.lista_peligros, "sugerencias": t.lista_sugerencias}
        for t in ServicioPersonalidad().tipos()
    ]})


@api_bp.get("/vark/preguntas")
def preguntas_vark():
    return jsonify({"ok": True, "preguntas": [
        {"numero": p.numero, "texto": p.texto,
         "opciones": [{"letra": o.letra, "texto": o.texto} for o in p.opciones]}
        for p in ServicioVark().preguntas()
    ]})
