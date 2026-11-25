"""
Envío de correos del formulario de contacto.
Responsable: Gerardo

Usa smtplib (incluido en Python). Para Gmail hay que crear una
"contraseña de aplicación" y ponerla en la variable MAIL_PASSWORD.
Si no hay correo configurado, el mensaje solo se guarda en la base de datos
y los administradores lo pueden leer en el panel.
"""
import smtplib
from email.message import EmailMessage


class ServicioCorreo:
    def __init__(self, config):
        self.servidor = config.get("MAIL_SERVER")
        self.puerto = config.get("MAIL_PORT")
        self.usuario = config.get("MAIL_USERNAME")
        self.password = config.get("MAIL_PASSWORD")
        self.destino = config.get("MAIL_DESTINO") or self.usuario

    @property
    def configurado(self) -> bool:
        return bool(self.usuario and self.password and self.destino)

    def enviar_contacto(self, nombre: str, email: str, asunto: str, mensaje: str) -> bool:
        if not self.configurado:
            return False
        correo = EmailMessage()
        correo["Subject"] = f"[VARK y Personalidad] {asunto}"
        correo["From"] = self.usuario
        correo["To"] = self.destino
        correo["Reply-To"] = email
        correo.set_content(
            f"Nuevo mensaje desde el sitio web\n\n"
            f"Nombre: {nombre}\nCorreo: {email}\nAsunto: {asunto}\n\n{mensaje}\n"
        )
        try:
            with smtplib.SMTP(self.servidor, self.puerto, timeout=15) as smtp:
                smtp.starttls()
                smtp.login(self.usuario, self.password)
                smtp.send_message(correo)
            return True
        except (smtplib.SMTPException, OSError):
            return False
