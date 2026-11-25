"""
Fábrica de la aplicación Flask.
Responsable: Gerardo
"""
import os
import secrets
from datetime import datetime

from flask import Flask, abort, render_template, request, session

from config import Config


def create_app(config_class=Config) -> Flask:
    from app.database import db

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    os.makedirs(app.instance_path, exist_ok=True)

    # 1) Base de datos (Singleton) + tablas + datos iniciales
    db.iniciar(app.config["DATABASE_URL"])
    db.crear_tablas()
    from app.data.semilla import CargadorDatos

    CargadorDatos().ejecutar(app.config["ADMIN_USUARIO"], app.config["ADMIN_PASSWORD"])
    db.cerrar_sesion()
    app.teardown_appcontext(db.cerrar_sesion)

    # 2) Rutas (blueprints)
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp
    from app.routes.auth import auth_bp
    from app.routes.instrumentos import instrumentos_bp
    from app.routes.publico import publico_bp

    app.register_blueprint(publico_bp)
    app.register_blueprint(instrumentos_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # 3) Protección CSRF sencilla para todos los formularios POST
    @app.before_request
    def proteger_csrf():
        if request.method == "POST" and not request.path.startswith("/api/"):
            token = session.get("csrf_token")
            if not token or token != request.form.get("csrf_token"):
                abort(400, description="El formulario expiró. Recarga la página e inténtalo de nuevo.")

    def csrf_token() -> str:
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(16)
        return session["csrf_token"]

    # 4) Variables disponibles en todas las plantillas
    @app.context_processor
    def variables_globales():
        from app.routes.auth import admin_actual

        from app.data.carreras import NOMBRES_CARRERAS, OPCION_OTRA

        return {
            "carreras_disponibles": NOMBRES_CARRERAS,
            "opcion_otra": OPCION_OTRA,
            "csrf_token": csrf_token,
            "admin_actual": admin_actual(),
            "anio_actual": datetime.now().year,
        }

    # 5) Páginas de error
    @app.errorhandler(404)
    def no_encontrado(_e):
        return render_template("errores/error.html", codigo=404,
                               mensaje="La página que buscas no existe."), 404

    @app.errorhandler(400)
    def peticion_invalida(e):
        return render_template("errores/error.html", codigo=400, mensaje=e.description), 400

    return app
