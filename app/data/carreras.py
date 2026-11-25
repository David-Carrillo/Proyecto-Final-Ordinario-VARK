"""
Catálogo de carreras para la lista desplegable.
Responsable: Lui

>>> Editen CARRERAS para que coincida con las carreras de su escuela. <<<
Cada carrera lleva sus siglas: si un alumno elige "Otra" y escribe "ISC",
"ingenieria en sistemas" o "Ing. Sistemas Computacionales", el sistema lo
guarda con el nombre oficial. Así las búsquedas por grupo no se separan.
"""
import difflib
import re
import unicodedata

# (nombre oficial, [siglas o nombres cortos que también se aceptan])
CARRERAS = [
    ("Ingeniería en Sistemas Computacionales", ["ISC", "Sistemas", "Sistemas Computacionales", "Ingeniería en Sistemas"]),
    ("Ingeniería en Tecnologías de la Información y Comunicaciones", ["TICS", "ITIC", "TIC"]),
    ("Ingeniería Informática", ["INF", "Informática"]),
    ("Ingeniería Industrial", ["IIND", "Industrial"]),
    ("Ingeniería en Gestión Empresarial", ["IGE", "Gestión Empresarial"]),
    ("Ingeniería Electrónica", ["IELC", "Electrónica"]),
    ("Ingeniería Mecatrónica", ["IMCT", "Mecatrónica"]),
    ("Ingeniería Mecánica", ["IMEC", "Mecánica"]),
    ("Ingeniería Civil", ["ICIV", "Civil"]),
    ("Ingeniería Química", ["IQUI", "Química"]),
    ("Licenciatura en Administración", ["LADM", "Administración"]),
    ("Contador Público", ["CP", "Contaduría"]),
    ("Arquitectura", ["ARQ"]),
]

NOMBRES_CARRERAS = [nombre for nombre, _ in CARRERAS]
OPCION_OTRA = "__otra__"


def _simplificar(texto: str) -> str:
    """'Ing. de Sistemas  Computacionales' -> 'ingenieria en sistemas computacionales'"""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c)).lower()
    texto = re.sub(r"[^a-z0-9 ]", " ", texto)
    texto = re.sub(r"\bing\b", "ingenieria", texto)
    texto = re.sub(r"\blic\b", "licenciatura", texto)
    texto = re.sub(r"\bde\b|\ben\b|\by\b|\bla\b", " ", texto)  # palabras de relleno
    return " ".join(texto.split())


_EXACTOS = {}
for _nombre, _alias in CARRERAS:
    _EXACTOS[_simplificar(_nombre)] = _nombre
    for _a in _alias:
        _EXACTOS[_simplificar(_a)] = _nombre


def normalizar_carrera(texto: str) -> str:
    """
    Regresa el nombre oficial si el texto corresponde a una carrera del catálogo
    (sin importar acentos, mayúsculas, siglas o un error de dedo pequeño).
    Si no se parece a ninguna, regresa el texto limpio tal como lo escribieron.
    """
    limpio = " ".join(texto.split())
    if not limpio:
        return ""
    simple = _simplificar(limpio)
    if simple in _EXACTOS:
        return _EXACTOS[simple]

    # Errores de dedo: solo si hay UNA carrera claramente parecida
    candidatos = {_simplificar(n): n for n in NOMBRES_CARRERAS}
    parecidos = difflib.get_close_matches(simple, list(candidatos), n=2, cutoff=0.88)
    if len(parecidos) == 1:
        return candidatos[parecidos[0]]
    if len(parecidos) == 2:
        r1 = difflib.SequenceMatcher(None, simple, parecidos[0]).ratio()
        r2 = difflib.SequenceMatcher(None, simple, parecidos[1]).ratio()
        if r1 - r2 >= 0.05:
            return candidatos[parecidos[0]]
    return limpio
