"""
Zona privada de administradores:
  - Panel principal
  - Mantenimiento (altas, bajas y cambios) de alumnos, administradores y
    tipos de personalidad; bajas de resultados y mensajes
  - Búsqueda de resultados por alumno, grupo o total
  - Dashboard con gráficas
  - PDF de la ficha técnica
Responsables: Gerardo (mantenimiento), Lui (búsqueda y PDF), Valeria (dashboard)
"""
from flask import Blueprint, abort, flash, make_response, redirect, render_template, request, url_for
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.database import db
from app.models import (
    Administrador,
    Alumno,
    MensajeContacto,
    ResultadoPersonalidad,
    ResultadoVark,
)
from app.routes.auth import admin_actual, login_requerido
from app.services.alumno_service import Filtro, ServicioAlumnos
from app.services.calculos import ESTILOS_VARK, ErrorValidacion
from app.services.estadisticas_service import Estadisticas
from app.services.personalidad_service import ServicioPersonalidad
from app.services.reporte_pdf import ReportePDF

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _contar(modelo) -> int:
    return db.sesion.scalar(select(func.count()).select_from(modelo))


# ------------------------------------------------------------------ PANEL
@admin_bp.route("/")
@login_requerido
def panel():
    resumen = {
        "alumnos": _contar(Alumno),
        "vark": _contar(ResultadoVark),
        "personalidad": _contar(ResultadoPersonalidad),
        "mensajes": _contar(MensajeContacto),
    }
    return render_template("admin/panel.html", resumen=resumen,
                           filtros=ServicioAlumnos().valores_distintos())


# --------------------------------------------------------------- ALUMNOS
@admin_bp.route("/alumnos")
@login_requerido
def alumnos():
    filtro = Filtro.desde_peticion(request.args)
    servicio = ServicioAlumnos()
    lista = servicio.buscar(filtro)
    return render_template("admin/alumnos.html", alumnos=lista, filtro=filtro,
                           filtros=servicio.valores_distintos())


@admin_bp.route("/alumnos/nuevo", methods=["GET", "POST"])
@admin_bp.route("/alumnos/<int:alumno_id>/editar", methods=["GET", "POST"])
@login_requerido
def alumno_form(alumno_id=None):
    servicio = ServicioAlumnos()
    alumno = servicio.por_id(alumno_id) if alumno_id else None
    if alumno_id and alumno is None:
        abort(404)

    if request.method == "POST":
        try:
            datos = servicio.validar_datos(request.form)
            otro = servicio.por_matricula(datos["matricula"])
            if otro and otro is not alumno:
                raise ErrorValidacion("Ya existe un alumno con esa matrícula.")
            if alumno is None:
                alumno = Alumno(**datos)
                db.sesion.add(alumno)
            else:
                for campo, valor in datos.items():
                    setattr(alumno, campo, valor)
            db.sesion.commit()
            flash("Alumno guardado correctamente.", "success")
            return redirect(url_for("admin.alumnos"))
        except ErrorValidacion as error:
            db.sesion.rollback()
            flash(str(error), "danger")

    return render_template("admin/alumno_form.html", alumno=alumno)


@admin_bp.route("/alumnos/<int:alumno_id>")
@login_requerido
def alumno_detalle(alumno_id):
    alumno = ServicioAlumnos().por_id(alumno_id) or abort(404)
    return render_template("admin/alumno_detalle.html", alumno=alumno, estilos=ESTILOS_VARK)


@admin_bp.route("/alumnos/<int:alumno_id>/eliminar", methods=["POST"])
@login_requerido
def alumno_eliminar(alumno_id):
    servicio = ServicioAlumnos()
    alumno = servicio.por_id(alumno_id) or abort(404)
    servicio.eliminar(alumno)
    flash("Alumno y sus resultados eliminados.", "info")
    return redirect(url_for("admin.alumnos"))


@admin_bp.route("/resultados/<tipo>/<int:resultado_id>/eliminar", methods=["POST"])
@login_requerido
def resultado_eliminar(tipo, resultado_id):
    modelo = {"vark": ResultadoVark, "personalidad": ResultadoPersonalidad}.get(tipo) or abort(404)
    resultado = db.sesion.get(modelo, resultado_id) or abort(404)
    alumno_id = resultado.alumno_id
    db.sesion.delete(resultado)
    db.sesion.commit()
    flash("Resultado eliminado.", "info")
    return redirect(url_for("admin.alumno_detalle", alumno_id=alumno_id))


# -------------------------------------------------------- ADMINISTRADORES
@admin_bp.route("/administradores")
@login_requerido
def administradores():
    lista = db.sesion.scalars(select(Administrador).order_by(Administrador.usuario)).all()
    return render_template("admin/administradores.html", administradores=lista)


@admin_bp.route("/administradores/nuevo", methods=["GET", "POST"])
@admin_bp.route("/administradores/<int:admin_id>/editar", methods=["GET", "POST"])
@login_requerido
def administrador_form(admin_id=None):
    admin = db.sesion.get(Administrador, admin_id) if admin_id else None
    if admin_id and admin is None:
        abort(404)

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        activo = bool(request.form.get("activo"))
        if not usuario or not nombre:
            flash("Usuario y nombre son obligatorios.", "danger")
        elif admin is None and len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "danger")
        elif password and len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "danger")
        elif admin is not None and admin.id == admin_actual().id and not activo:
            flash("No puedes desactivar tu propia cuenta.", "danger")
        else:
            if admin is None:
                admin = Administrador()
                db.sesion.add(admin)
            admin.usuario, admin.nombre, admin.email, admin.activo = usuario, nombre, email, activo
            if password:
                admin.establecer_password(password)
            try:
                db.sesion.commit()
                flash("Administrador guardado.", "success")
                return redirect(url_for("admin.administradores"))
            except IntegrityError:
                db.sesion.rollback()
                flash("Ese nombre de usuario ya existe.", "danger")

    return render_template("admin/administrador_form.html", admin=admin)


@admin_bp.route("/administradores/<int:admin_id>/eliminar", methods=["POST"])
@login_requerido
def administrador_eliminar(admin_id):
    admin = db.sesion.get(Administrador, admin_id) or abort(404)
    if admin.id == admin_actual().id:
        flash("No puedes eliminar tu propia cuenta.", "danger")
    else:
        db.sesion.delete(admin)
        db.sesion.commit()
        flash("Administrador eliminado.", "info")
    return redirect(url_for("admin.administradores"))


# ------------------------------------------------- TIPOS DE PERSONALIDAD
@admin_bp.route("/tipos")
@login_requerido
def tipos():
    return render_template("admin/tipos.html", tipos=ServicioPersonalidad().tipos())


@admin_bp.route("/tipos/<codigo>/editar", methods=["GET", "POST"])
@login_requerido
def tipo_form(codigo):
    tipo = ServicioPersonalidad().tipo(codigo) or abort(404)
    if request.method == "POST":
        peligros = request.form.get("peligros", "").strip()
        sugerencias = request.form.get("sugerencias", "").strip()
        if not peligros or not sugerencias:
            flash("Los dos campos son obligatorios.", "danger")
        else:
            tipo.peligros, tipo.sugerencias = peligros, sugerencias
            db.sesion.commit()
            flash(f"Tipo {tipo.codigo} actualizado.", "success")
            return redirect(url_for("admin.tipos"))
    return render_template("admin/tipo_form.html", tipo=tipo)


# ------------------------------------------------------------- MENSAJES
@admin_bp.route("/mensajes")
@login_requerido
def mensajes():
    lista = db.sesion.scalars(select(MensajeContacto).order_by(MensajeContacto.fecha.desc())).all()
    return render_template("admin/mensajes.html", mensajes=lista)


@admin_bp.route("/mensajes/<int:mensaje_id>/eliminar", methods=["POST"])
@login_requerido
def mensaje_eliminar(mensaje_id):
    mensaje = db.sesion.get(MensajeContacto, mensaje_id) or abort(404)
    db.sesion.delete(mensaje)
    db.sesion.commit()
    flash("Mensaje eliminado.", "info")
    return redirect(url_for("admin.mensajes"))


# ------------------------------------------------- BÚSQUEDA Y DASHBOARD
@admin_bp.route("/dashboard")
@login_requerido
def dashboard():
    filtro = Filtro.desde_peticion(request.args)
    servicio = ServicioAlumnos()
    lista = servicio.buscar(filtro)
    resumen = Estadisticas(lista).resumen()
    return render_template("admin/dashboard.html", filtro=filtro, alumnos=lista,
                           resumen=resumen, estilos=ESTILOS_VARK,
                           filtros=servicio.valores_distintos())


@admin_bp.route("/reporte.pdf")
@login_requerido
def reporte_pdf():
    filtro = Filtro.desde_peticion(request.args)
    lista = ServicioAlumnos().buscar(filtro)
    reporte = ReportePDF()
    if filtro.ambito == "individual" and len(lista) == 1:
        pdf = reporte.individual(lista[0])
        nombre = f"ficha_{lista[0].matricula}.pdf"
    else:
        pdf = reporte.grupal(lista, filtro.titulo)
        nombre = "ficha_grupal.pdf" if filtro.ambito == "grupal" else "ficha_total.pdf"
    respuesta = make_response(pdf)
    respuesta.headers["Content-Type"] = "application/pdf"
    respuesta.headers["Content-Disposition"] = f'inline; filename="{nombre}"'
    return respuesta
