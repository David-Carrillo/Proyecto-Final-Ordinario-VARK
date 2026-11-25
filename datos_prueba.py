"""
Carga alumnos de prueba con respuestas al azar, para probar dashboards,
búsquedas y PDF. Responsable: Gerardo (implementación)

Uso:
    python datos_prueba.py          (crea 30 alumnos)
    python datos_prueba.py 60       (crea 60 alumnos)

Además registra los dos ejemplos resueltos de los PDF:
    matrícula EJ-VARK   → VARK 7-4-5-5 (Visual)
    matrícula EJ-ISTJ   → personalidad ISTJ
"""
import random
import sys

from app import create_app
from app.data.instrumentos import CLAVE_VARK
from app.database import db
from app.services.alumno_service import ServicioAlumnos
from app.services.personalidad_service import ServicioPersonalidad
from app.services.vark_service import ServicioVark

NOMBRES = ["Ana", "Luis", "María", "Jorge", "Sofía", "Diego", "Valeria", "Carlos", "Fernanda",
           "Miguel", "Daniela", "José", "Camila", "Andrés", "Paola", "Ricardo", "Ximena", "Emilio"]
APELLIDOS = ["García", "Hernández", "López", "Martínez", "González", "Pérez", "Rodríguez",
             "Sánchez", "Ramírez", "Cruz", "Flores", "Morales", "Ortiz", "Reyes"]
GRUPOS = [("Ingeniería en Sistemas Computacionales", 5, "A"),
          ("Ingeniería en Sistemas Computacionales", 5, "B"),
          ("Licenciatura en Administración", 3, "A")]

EJEMPLO_VARK = {1: "b", 2: "c", 3: "b", 4: "c", 5: "a", 6: "c", 7: "c", 8: "ba", 9: "ab",
                10: "a", 11: "a", 12: "c", 13: "da", 14: "ca", 15: "d", 16: "ab"}
EJEMPLO_ISTJ = {1: [7, 0, 0, 7, 4, 4, 4, 2, 4], 2: [6, 6, 6, 4, 4, 6, 4, 9, 7],
                3: [1, 6, 4, 8, 9, 9, 9, 9, 9], 4: [10, 6, 7, 9, 9, 9, 10, 9, 9]}


def opciones_vark(preguntas, elegir):
    """elegir(numero_pregunta) -> letras elegidas"""
    ids = []
    for p in preguntas:
        letras = elegir(p.numero)
        ids += [o.id for o in p.opciones if o.letra in letras]
    return ids


def main(cantidad: int) -> None:
    create_app()
    alumnos, vark, pers = ServicioAlumnos(), ServicioVark(), ServicioPersonalidad()
    preguntas = vark.preguntas()
    reactivos = pers.reactivos_por_dimension()
    valores = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10]

    for i in range(1, cantidad + 1):
        carrera, semestre, grupo = random.choice(GRUPOS)
        alumno = alumnos.registrar_o_actualizar({
            "matricula": f"PRU{i:04d}",
            "nombre": f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)} {random.choice(APELLIDOS)}",
            "carrera": carrera, "semestre": str(semestre), "grupo": grupo,
        })
        # Cada alumno tiene un estilo "favorito" para que las gráficas se vean variadas
        favorito = random.randrange(4)

        def elegir(numero):
            clave = CLAVE_VARK[numero]
            letras = {clave[favorito]} if random.random() < 0.6 else {random.choice("abcd")}
            if random.random() < 0.2:
                letras.add(random.choice("abcd"))
            return letras

        vark.registrar(alumno, opciones_vark(preguntas, elegir))

        sesgo = [random.choice([True, False]) for _ in range(4)]
        puntos = {}
        for d, lista in reactivos.items():
            for r in lista:
                a = random.choice([6, 7, 8, 9, 10] if sesgo[d - 1] else [0, 1, 2, 3, 4])
                if random.random() < 0.25:
                    a = random.choice(valores)
                puntos[r.id] = (a, 10 - a)
        pers.registrar(alumno, puntos)

    # Ejemplos resueltos de los PDF
    ejemplo = alumnos.registrar_o_actualizar({"matricula": "EJ-VARK", "nombre": "Ejemplo PDF VARK",
                                              "carrera": "Ejemplos", "semestre": "1", "grupo": "PDF"})
    vark.registrar(ejemplo, opciones_vark(preguntas, lambda n: set(EJEMPLO_VARK[n])))
    ejemplo = alumnos.registrar_o_actualizar({"matricula": "EJ-ISTJ", "nombre": "Ejemplo PDF Personalidad",
                                              "carrera": "Ejemplos", "semestre": "1", "grupo": "PDF"})
    puntos = {r.id: (EJEMPLO_ISTJ[d][r.orden - 1], 10 - EJEMPLO_ISTJ[d][r.orden - 1])
              for d, lista in reactivos.items() for r in lista}
    resultado = pers.registrar(ejemplo, puntos)
    db.cerrar_sesion()
    print(f"Listo: {cantidad} alumnos de prueba + 2 ejemplos. El ejemplo ISTJ dio: {resultado.tipo_codigo}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 30)
