"""
Páginas públicas: inicio, acerca de (video y audio) y contacto.
Responsable: Gerardo
"""
import re

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from app.data.instrumentos import DESCRIPCION_VARK
from app.database import db
from app.models import MensajeContacto
from app.services.calculos import ESTILOS_VARK, TEMPERAMENTOS
from app.services.correo_service import ServicioCorreo

publico_bp = Blueprint("publico", __name__)

PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@publico_bp.route("/")
def inicio():
    return render_template(
        "index.html",
        estilos=ESTILOS_VARK,
        descripciones=DESCRIPCION_VARK,
        temperamentos=TEMPERAMENTOS,
    )


@publico_bp.route("/acerca")
def acerca():
    return render_template("acerca.html")


@publico_bp.route("/contacto", methods=["GET", "POST"])
def contacto():
    datos = {"nombre": "", "email": "", "asunto": "", "mensaje": ""}
    if request.method == "POST":
        datos = {k: request.form.get(k, "").strip() for k in datos}
        errores = []
        if not all(datos.values()):
            errores.append("Todos los campos son obligatorios.")
        if datos["email"] and not PATRON_EMAIL.match(datos["email"]):
            errores.append("El correo electrónico no es válido.")
        if len(datos["mensaje"]) > 2000:
            errores.append("El mensaje no puede pasar de 2000 caracteres.")

        if errores:
            for e in errores:
                flash(e, "danger")
        else:
            correo = ServicioCorreo(current_app.config)
            enviado = correo.enviar_contacto(**datos)
            db.sesion.add(MensajeContacto(**datos, enviado=enviado))
            db.sesion.commit()
            flash("¡Gracias! Tu mensaje fue recibido, te responderemos pronto.", "success")
            return redirect(url_for("publico.contacto"))

    return render_template("contacto.html", datos=datos)
