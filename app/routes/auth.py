"""
Autenticación de administradores (zona pública / zona privada).
Responsable: Gerardo
"""
from functools import wraps

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import select

from app.database import db
from app.models import Administrador

auth_bp = Blueprint("auth", __name__, url_prefix="/admin")


def admin_actual():
    """Regresa el administrador con sesión iniciada o None."""
    if "admin" not in g:
        admin_id = session.get("admin_id")
        admin = db.sesion.get(Administrador, admin_id) if admin_id else None
        g.admin = admin if admin and admin.activo else None
    return g.admin


def login_requerido(vista):
    """Decorador: solo deja pasar a administradores con sesión iniciada."""

    @wraps(vista)
    def envoltura(*args, **kwargs):
        if admin_actual() is None:
            flash("Inicia sesión como administrador para continuar.", "warning")
            return redirect(url_for("auth.login", siguiente=request.path))
        return vista(*args, **kwargs)

    return envoltura


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if admin_actual():
        return redirect(url_for("admin.panel"))

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")
        admin = db.sesion.scalar(select(Administrador).where(Administrador.usuario == usuario))
        if admin and admin.activo and admin.verificar_password(password):
            session.clear()
            session["admin_id"] = admin.id
            session.permanent = bool(request.form.get("recordar"))
            flash(f"Bienvenido, {admin.nombre}.", "success")
            siguiente = request.args.get("siguiente", "")
            # Solo se permiten redirecciones internas
            if siguiente.startswith("/") and not siguiente.startswith("//"):
                return redirect(siguiente)
            return redirect(url_for("admin.panel"))
        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("admin/login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("admin_id", None)
    flash("Sesión cerrada.", "info")
    return redirect(url_for("publico.inicio"))
