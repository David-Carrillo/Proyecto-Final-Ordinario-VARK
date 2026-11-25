"""
Aplicación de los instrumentos (VARK y personalidad), resultados individuales
y consulta pública por matrícula.
Responsables: Lui (cálculo y registro) y Valeria (formularios)

Aplicación GRUPAL: el profesor comparte un enlace con los datos del grupo,
por ejemplo  /vark?carrera=Sistemas&semestre=5&grupo=A
y el formulario aparece con esos datos ya llenos para todo el grupo.
"""
from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for, make_response

from app.data.instrumentos import DESCRIPCION_VARK, ESTRATEGIAS_VARK
from app.database import db
from app.routes.auth import admin_actual
from app.services.alumno_service import ServicioAlumnos
from app.services.calculos import (
    DIMENSIONES,
    ESTILOS_VARK,
    NOMBRES_LETRAS,
    CalculadoraPersonalidad,
    CalculadoraVark,
    ErrorValidacion,
)
from app.services.personalidad_service import ServicioPersonalidad
from app.services.reporte_pdf import ReportePDF
from app.services.vark_service import ServicioVark

instrumentos_bp = Blueprint("instrumentos", __name__)

CAMPOS_ALUMNO = ("matricula", "nombre", "carrera", "semestre", "grupo")


def _datos_alumno_iniciales() -> dict:
    """Toma los datos del grupo de la URL (aplicación grupal)."""
    return {campo: request.args.get(campo, "") for campo in CAMPOS_ALUMNO}


def _recordar_resultado(clave: str, resultado_id: int) -> None:
    """Guarda en la sesión qué resultados puede ver este navegador."""
    lista = session.get(clave, [])
    lista.append(resultado_id)
    session[clave] = lista[-20:]


def _puede_ver(clave: str, resultado_id: int) -> bool:
    return admin_actual() is not None or resultado_id in session.get(clave, [])


# ----------------------------------------------------------------- VARK
@instrumentos_bp.route("/vark", methods=["GET", "POST"])
def vark():
    servicio = ServicioVark()
    datos = _datos_alumno_iniciales()
    seleccion: set = set()

    if request.method == "POST":
        datos = {campo: request.form.get(campo, "") for campo in CAMPOS_ALUMNO}
        seleccion = set(request.form.getlist("opciones"))
        try:
            alumno = ServicioAlumnos().registrar_o_actualizar(datos)
            resultado = servicio.registrar(alumno, list(seleccion))
            _recordar_resultado("mis_vark", resultado.id)
            flash("¡Listo! Este es tu resultado.", "success")
            return redirect(url_for("instrumentos.resultado_vark", resultado_id=resultado.id))
        except ErrorValidacion as error:
            db.sesion.rollback()
            flash(str(error), "danger")

    return render_template("vark/formulario.html", preguntas=servicio.preguntas(),
                           datos=datos, seleccion=seleccion)


@instrumentos_bp.route("/vark/resultado/<int:resultado_id>")
def resultado_vark(resultado_id):
    if not _puede_ver("mis_vark", resultado_id):
        abort(404)
    resultado = ServicioVark().obtener(resultado_id) or abort(404)
    return render_template(
        "vark/resultado.html",
        resultado=resultado,
        estilos=ESTILOS_VARK,
        porcentajes=CalculadoraVark.porcentajes(resultado.conteo),
        estrategias=ESTRATEGIAS_VARK,
        descripciones=DESCRIPCION_VARK,
    )


# --------------------------------------------------------- PERSONALIDAD
@instrumentos_bp.route("/personalidad", methods=["GET", "POST"])
def personalidad():
    servicio = ServicioPersonalidad()
    reactivos = servicio.reactivos_por_dimension()
    datos = _datos_alumno_iniciales()
    puntos_previos: dict = {}

    if request.method == "POST":
        datos = {campo: request.form.get(campo, "") for campo in CAMPOS_ALUMNO}
        puntos = {}
        for lista in reactivos.values():
            for r in lista:
                a = request.form.get(f"a_{r.id}", "")
                b = request.form.get(f"b_{r.id}", "")
                if a != "" and b != "":
                    puntos[r.id] = (a, b)
                    puntos_previos[r.id] = a
        try:
            alumno = ServicioAlumnos().registrar_o_actualizar(datos)
            resultado = servicio.registrar(alumno, puntos)
            _recordar_resultado("mis_personalidad", resultado.id)
            flash("¡Listo! Este es tu resultado.", "success")
            return redirect(url_for("instrumentos.resultado_personalidad", resultado_id=resultado.id))
        except ErrorValidacion as error:
            db.sesion.rollback()
            flash(str(error), "danger")

    return render_template("personalidad/formulario.html", reactivos=reactivos,
                           dimensiones=DIMENSIONES, nombres=NOMBRES_LETRAS,
                           datos=datos, puntos_previos=puntos_previos)


@instrumentos_bp.route("/personalidad/resultado/<int:resultado_id>")
def resultado_personalidad(resultado_id):
    if not _puede_ver("mis_personalidad", resultado_id):
        abort(404)
    resultado = ServicioPersonalidad().obtener(resultado_id) or abort(404)
    return render_template(
        "personalidad/resultado.html",
        resultado=resultado,
        dimensiones=DIMENSIONES,
        nombres=NOMBRES_LETRAS,
        temperamento=CalculadoraPersonalidad.temperamento(resultado.tipo_codigo),
    )


@instrumentos_bp.route("/personalidad/tipos")
def tipos():
    return render_template("personalidad/tipos.html", tipos=ServicioPersonalidad().tipos())


# ------------------------------------------------- CONSULTA POR MATRÍCULA
@instrumentos_bp.route("/consultar")
def consultar():
    matricula = request.args.get("matricula", "").strip()
    alumno = ServicioAlumnos().por_matricula(matricula) if matricula else None
    if matricula and alumno is None:
        flash("No encontramos resultados con esa matrícula.", "warning")
    if alumno:
        # Permite abrir los resultados de este alumno desde este navegador
        for r in alumno.resultados_vark:
            if r.id not in session.get("mis_vark", []):
                _recordar_resultado("mis_vark", r.id)
        for r in alumno.resultados_personalidad:
            if r.id not in session.get("mis_personalidad", []):
                _recordar_resultado("mis_personalidad", r.id)
    return render_template("consulta/consultar.html", matricula=matricula, alumno=alumno,
                           estilos=ESTILOS_VARK)


@instrumentos_bp.route("/consultar/<matricula>/pdf")
def consultar_pdf(matricula):
    alumno = ServicioAlumnos().por_matricula(matricula) or abort(404)
    pdf = ReportePDF().individual(alumno)
    respuesta = make_response(pdf)
    respuesta.headers["Content-Type"] = "application/pdf"
    respuesta.headers["Content-Disposition"] = f'inline; filename="ficha_{alumno.matricula}.pdf"'
    return respuesta
