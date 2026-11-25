"""
Estadísticas para los dashboards y el PDF (individual, grupal o total).
Responsable: Lui

Se toma el ÚLTIMO resultado de cada alumno para no contar dos veces
a quien contestó el test más de una vez.
"""
from collections import Counter

from app.services.calculos import (
    ESTILOS_VARK,
    TEMPERAMENTOS,
    CalculadoraVark,
)


class Estadisticas:
    def __init__(self, alumnos):
        self.alumnos = list(alumnos)
        self.vark = [a.ultimo_vark for a in self.alumnos if a.ultimo_vark]
        self.personalidad = [
            a.ultima_personalidad for a in self.alumnos if a.ultima_personalidad
        ]

    # ------------------------------------------------------------------ VARK
    def vark_suma(self) -> dict:
        """Suma de puntos de cada estilo de todos los alumnos."""
        suma = {k: 0 for k in "VARK"}
        for r in self.vark:
            for k, v in r.conteo.items():
                suma[k] += v
        return suma

    def vark_promedio(self) -> dict:
        n = len(self.vark) or 1
        return {k: round(v / n, 2) for k, v in self.vark_suma().items()}

    def vark_dominantes(self) -> dict:
        """Cuántos alumnos tienen cada estilo dominante (multimodal aparte)."""
        cuenta = Counter()
        for r in self.vark:
            if len(r.estilo_dominante) == 1:
                cuenta[r.estilo_dominante] += 1
            else:
                cuenta["M"] += 1
        etiquetas = dict(ESTILOS_VARK, M="Multimodal")
        return {etiquetas[k]: cuenta.get(k, 0) for k in "VARKM"}

    def vark_dominante_global(self) -> str:
        suma = self.vark_suma()
        if not any(suma.values()):
            return "Sin datos"
        maximo = max(suma.values())
        letras = "".join(k for k in "VARK" if suma[k] == maximo)
        return CalculadoraVark.describir(letras)

    # ---------------------------------------------------------- PERSONALIDAD
    def personalidad_tipos(self) -> dict:
        cuenta = Counter(r.tipo_codigo for r in self.personalidad)
        return dict(sorted(cuenta.items(), key=lambda x: (-x[1], x[0])))

    def personalidad_letras(self) -> dict:
        """Cuántos alumnos tienen cada preferencia (E vs I, S vs N, ...)."""
        cuenta = {letra: 0 for letra in "EISNTFJP"}
        for r in self.personalidad:
            for letra in r.tipo_codigo:
                cuenta[letra] += 1
        return cuenta

    def personalidad_promedios(self) -> dict:
        n = len(self.personalidad) or 1
        suma = {letra: 0 for letra in "EISNTFJP"}
        for r in self.personalidad:
            for letra, valor in r.totales.items():
                suma[letra] += valor
        return {k: round(v / n, 1) for k, v in suma.items()}

    def personalidad_temperamentos(self) -> dict:
        cuenta = Counter()
        for r in self.personalidad:
            clave = r.tipo_codigo[1] + r.tipo_codigo[2]
            cuenta[TEMPERAMENTOS[clave]["nombre"]] += 1
        return {t["nombre"]: cuenta.get(t["nombre"], 0) for t in TEMPERAMENTOS.values()}

    def tipo_mas_comun(self) -> str:
        tipos = self.personalidad_tipos()
        return next(iter(tipos)) if tipos else "Sin datos"

    # --------------------------------------------------------------- resumen
    def resumen(self) -> dict:
        return {
            "total_alumnos": len(self.alumnos),
            "con_vark": len(self.vark),
            "con_personalidad": len(self.personalidad),
            "vark": {
                "suma": self.vark_suma(),
                "promedio": self.vark_promedio(),
                "dominantes": self.vark_dominantes(),
                "dominante_global": self.vark_dominante_global(),
            },
            "personalidad": {
                "tipos": self.personalidad_tipos(),
                "letras": self.personalidad_letras(),
                "promedios": self.personalidad_promedios(),
                "temperamentos": self.personalidad_temperamentos(),
                "tipo_mas_comun": self.tipo_mas_comun(),
            },
        }
