"""
Pruebas unitarias de los cálculos, usando los ejemplos resueltos de los PDF.
Responsable: Lui (con apoyo de todo el equipo)

Ejecutar desde la carpeta del proyecto:
    python -m unittest discover -s tests -v
"""
import os
import sys
import unittest
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.data.instrumentos import (  # noqa: E402
    CLAVE_VARK,
    PREGUNTAS_VARK,
    REACTIVOS_PERSONALIDAD,
    TIPOS_PERSONALIDAD,
    estilo_de_opcion,
)
from app.services.calculos import (  # noqa: E402
    DIMENSIONES,
    CalculadoraPersonalidad,
    CalculadoraVark,
    ErrorValidacion,
)
from app.services.estadisticas_service import Estadisticas  # noqa: E402
from app.data.carreras import NOMBRES_CARRERAS, normalizar_carrera  # noqa: E402

# Respuestas encerradas en círculo en el ejemplo del PDF de VARK (pág. 89)
EJEMPLO_VARK = {
    1: ["b"], 2: ["c"], 3: ["b"], 4: ["c"], 5: ["a"], 6: ["c"], 7: ["c"],
    8: ["b", "a"], 9: ["a", "b"], 10: ["a"], 11: ["a"], 12: ["c"],
    13: ["d", "a"], 14: ["c", "a"], 15: ["d"], 16: ["a", "b"],
}

# Puntos de la columna izquierda del ejemplo del PDF de personalidad (pág. 6)
EJEMPLO_PERSONALIDAD = {
    1: [7, 0, 0, 7, 4, 4, 4, 2, 4],     # E (I = 10 - E)
    2: [6, 6, 6, 4, 4, 6, 4, 9, 7],     # S
    3: [1, 6, 4, 8, 9, 9, 9, 9, 9],     # T
    4: [10, 6, 7, 9, 9, 9, 10, 9, 9],   # J
}


def respuestas_personalidad(puntos_izquierda):
    filas = []
    for d, puntos in puntos_izquierda.items():
        a, b, _ = DIMENSIONES[d]
        for p in puntos:
            filas.append((a, p, b, 10 - p))
    return filas


class PruebasInstrumentos(unittest.TestCase):
    def test_vark_tiene_16_preguntas_con_4_opciones(self):
        self.assertEqual(len(PREGUNTAS_VARK), 16)
        for numero, _texto, opciones in PREGUNTAS_VARK:
            self.assertEqual([o[0] for o in opciones], ["a", "b", "c", "d"], numero)

    def test_clave_vark_asigna_un_estilo_distinto_a_cada_opcion(self):
        for numero, clave in CLAVE_VARK.items():
            self.assertEqual(sorted(clave), ["a", "b", "c", "d"], numero)

    def test_personalidad_tiene_4_dimensiones_de_9_renglones(self):
        self.assertEqual(sorted(REACTIVOS_PERSONALIDAD), [1, 2, 3, 4])
        for renglones in REACTIVOS_PERSONALIDAD.values():
            self.assertEqual(len(renglones), 9)

    def test_hay_16_tipos_distintos(self):
        codigos = {t[1] for t in TIPOS_PERSONALIDAD}
        self.assertEqual(len(codigos), 16)
        for _n, codigo, peligros, sugerencias in TIPOS_PERSONALIDAD:
            self.assertTrue(peligros and sugerencias, codigo)


class PruebasVark(unittest.TestCase):
    def test_ejemplo_del_pdf_da_7_4_5_5(self):
        estilos = [estilo_de_opcion(p, l) for p, letras in EJEMPLO_VARK.items() for l in letras]
        conteo, dominante = CalculadoraVark.calcular(estilos)
        self.assertEqual(conteo, {"V": 7, "A": 4, "R": 5, "K": 5})
        self.assertEqual(dominante, "V")
        self.assertEqual(CalculadoraVark.describir(dominante), "Visual")

    def test_empate_es_multimodal(self):
        conteo, dominante = CalculadoraVark.calcular(["V", "K", "V", "K", "A"])
        self.assertEqual(dominante, "VK")
        self.assertEqual(CalculadoraVark.describir(dominante), "Multimodal (Visual, Kinestésico)")

    def test_sin_respuestas_es_error(self):
        with self.assertRaises(ErrorValidacion):
            CalculadoraVark.calcular([])

    def test_porcentajes(self):
        self.assertEqual(CalculadoraVark.porcentajes({"V": 1, "A": 1, "R": 1, "K": 1})["V"], 25.0)


class PruebasPersonalidad(unittest.TestCase):
    def test_ejemplo_del_pdf_da_istj(self):
        totales, tipo = CalculadoraPersonalidad.calcular(respuestas_personalidad(EJEMPLO_PERSONALIDAD))
        self.assertEqual(totales, {"E": 32, "I": 58, "S": 52, "N": 38,
                                   "T": 64, "F": 26, "J": 78, "P": 12})
        self.assertEqual(tipo, "ISTJ")
        self.assertEqual(CalculadoraPersonalidad.temperamento(tipo)["nombre"], "Técnico analítico")

    def test_no_se_permite_el_5(self):
        with self.assertRaises(ErrorValidacion):
            CalculadoraPersonalidad.validar_par(5, 5)

    def test_el_par_debe_sumar_10(self):
        with self.assertRaises(ErrorValidacion):
            CalculadoraPersonalidad.validar_par(7, 4)

    def test_fuera_de_rango(self):
        with self.assertRaises(ErrorValidacion):
            CalculadoraPersonalidad.validar_par(11, -1)

    def test_valores_no_numericos(self):
        with self.assertRaises(ErrorValidacion):
            CalculadoraPersonalidad.validar_par("a", "b")

    def test_empate_elige_segunda_letra(self):
        # 45 / 45 en E-I: gana I
        filas = [("E", p, "I", 10 - p) for p in (6, 6, 6, 6, 6, 4, 4, 4, 3)]
        totales, _ = CalculadoraPersonalidad.calcular(filas)
        self.assertEqual(totales["E"], totales["I"])
        _, tipo = CalculadoraPersonalidad.calcular(filas + respuestas_personalidad(
            {2: [6] * 9, 3: [6] * 9, 4: [6] * 9}))
        self.assertEqual(tipo, "ISTJ")


class PruebasEstadisticas(unittest.TestCase):
    def _alumno(self, conteo, dominante, tipo, totales):
        vark = SimpleNamespace(conteo=conteo, estilo_dominante=dominante)
        pers = SimpleNamespace(tipo_codigo=tipo, totales=totales)
        return SimpleNamespace(ultimo_vark=vark, ultima_personalidad=pers)

    def test_resumen_grupal(self):
        t = {"E": 32, "I": 58, "S": 52, "N": 38, "T": 64, "F": 26, "J": 78, "P": 12}
        alumnos = [
            self._alumno({"V": 7, "A": 4, "R": 5, "K": 5}, "V", "ISTJ", t),
            self._alumno({"V": 2, "A": 6, "R": 2, "K": 6}, "AK", "ENFP", t),
            SimpleNamespace(ultimo_vark=None, ultima_personalidad=None),
        ]
        r = Estadisticas(alumnos).resumen()
        self.assertEqual(r["total_alumnos"], 3)
        self.assertEqual(r["con_vark"], 2)
        self.assertEqual(r["vark"]["suma"], {"V": 9, "A": 10, "R": 7, "K": 11})
        self.assertEqual(r["vark"]["dominantes"]["Visual"], 1)
        self.assertEqual(r["vark"]["dominantes"]["Multimodal"], 1)
        self.assertEqual(r["vark"]["dominante_global"], "Kinestésico")
        self.assertEqual(r["personalidad"]["tipos"], {"ENFP": 1, "ISTJ": 1})
        self.assertEqual(r["personalidad"]["temperamentos"]["Técnico analítico"], 1)
        self.assertEqual(r["personalidad"]["temperamentos"]["Social"], 1)
        self.assertEqual(r["personalidad"]["letras"]["I"], 1)


class PruebasCarreras(unittest.TestCase):
    ISC = "Ingeniería en Sistemas Computacionales"

    def test_siglas_y_variantes_dan_el_nombre_oficial(self):
        for texto in ["ISC", "isc", "Ing. Sistemas Computacionales", "ingeniera de sistemas computacionales",
                      "INGENIERIA EN SISTEMAS COMPUTACIONALES", "Ingeniería en Sistemas"]:
            self.assertEqual(normalizar_carrera(texto), self.ISC, texto)

    def test_carreras_parecidas_no_se_confunden(self):
        self.assertEqual(normalizar_carrera("ingenieria mecanica"), "Ingeniería Mecánica")
        self.assertEqual(normalizar_carrera("ingenieria mecatronica"), "Ingeniería Mecatrónica")

    def test_carrera_que_no_esta_en_la_lista_se_respeta(self):
        self.assertEqual(normalizar_carrera("  Medicina   Veterinaria "), "Medicina Veterinaria")

    def test_nombres_oficiales_no_cambian(self):
        for nombre in NOMBRES_CARRERAS:
            self.assertEqual(normalizar_carrera(nombre), nombre)


if __name__ == "__main__":
    unittest.main()
