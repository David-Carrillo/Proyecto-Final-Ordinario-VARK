"""
Punto de entrada de la aplicación.
Responsable: Gerardo

Uso:
    python run.py
Después abre http://127.0.0.1:5000 en el navegador.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
