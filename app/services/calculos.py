"""
Lógica de cálculo de los dos instrumentos.
Responsable: Lui

Este archivo NO depende de la base de datos para poder probarlo solo
(ver tests/test_calculos.py).

VARK
----
Cada opción de cada pregunta pertenece a un estilo (V, A, R o K) según la
tabla "Estilo prevaleciente de acuerdo a la respuesta seleccionada" del PDF.
Se puede elegir más de una opción por pregunta o dejarla en blanco.
El resultado es cuántas veces se eligió cada estilo. El estilo con más
puntos es el dominante; si hay empate, el alumno es multimodal.

Ejemplo del PDF: V=7, A=4, R=5, K=5  →  dominante: Visual.

Personalidad (Jung / Myers-Briggs)
----------------------------------
Hay 4 dimensiones con 9 renglones cada una. En cada renglón se reparten
10 puntos entre la frase de la columna A y la de la columna C, sin usar el 5
(así siempre gana una de las dos). Se suman los puntos de cada letra y en
cada dimensión gana la letra con más puntos.

    1. E / I   Energía, focalización y actitud vital
    2. S / N   Manejo de la información
    3. T / F   Actitud y toma de decisiones
    4. J / P   Ambiente de trabajo y estilo de vida

Ejemplo del PDF: E=32 I=58, S=52 N=38, T=64 F=26, J=78 P=12  →  ISTJ.
"""

ESTILOS_VARK = {
    "V": "Visual",
    "A": "Auditivo",
    "R": "Lectura/Escritura",
    "K": "Kinestésico",
}

DIMENSIONES = {
    1: ("E", "I", "Energía, focalización y actitud vital"),
    2: ("S", "N", "Manejo de la información y actitud ante el entorno"),
    3: ("T", "F", "Actitud y toma de decisiones"),
    4: ("J", "P", "Ambiente de trabajo, estilo de vida en el entorno e interacción"),
}

NOMBRES_LETRAS = {
    "E": "Extrovertido", "I": "Introvertido",
    "S": "Sensorial", "N": "Intuitivo",
    "T": "Racional", "F": "Emocional",
    "J": "Calificador (Juicio)", "P": "Perceptivo",
}

# Enfoque de P. Denichaud: combinación de la forma de captar información
# (S/N) y la forma de decidir (T/F).
TEMPERAMENTOS = {
    "ST": {
        "nombre": "Técnico analítico",
        "rasgos": [
            "Pensadores y analistas lógicos.",
            "Interés por las realidades y los hechos concretos.",
            "Capacidad para recibir, clasificar y ordenar información.",
            "Respetuosos de técnicas y métodos.",
            "No cambian fácilmente su lógica.",
            "Tendencia al perfeccionismo.",
        ],
        "motivador": "El respeto",
        "evitar": "El ridículo",
    },
    "NT": {
        "nombre": "Controlador",
        "rasgos": [
            "Trazan estrategias y controlan sistemas.",
            "Necesitan información.",
            "Tratan de convencer.",
            "Sugieren con frecuencia.",
        ],
        "motivador": "El poder",
        "evitar": "Perder el tiempo",
    },
    "SF": {
        "nombre": "Apoyo",
        "rasgos": [
            "Empáticos, sinceros.",
            "Tratan que todos estén contentos.",
            "Tienden a ser protectores.",
            "Rechazan la desconfianza.",
            "Aglutinan colectivos y generan armonía.",
            "Mediadores naturales.",
        ],
        "motivador": "La aprobación",
        "evitar": "Perder una relación",
    },
    "NF": {
        "nombre": "Social",
        "rasgos": [
            "Joviales.",
            "Logran fácilmente ser el centro.",
            "Tienden al optimismo.",
            "Facilidad para entablar relaciones.",
        ],
        "motivador": "El reconocimiento",
        "evitar": "Perder su esfuerzo",
    },
}


class ErrorValidacion(ValueError):
    """Se lanza cuando las respuestas no cumplen las reglas del instrumento."""


class CalculadoraVark:
    """Calcula el resultado del cuestionario VARK."""

    ORDEN = "VARK"

    @classmethod
    def calcular(cls, estilos_elegidos) -> tuple[dict, str]:
        """
        Recibe la lista de estilos de las opciones marcadas,
        por ejemplo ["V", "R", "V", "K", ...].
        Regresa (conteo, dominante), por ejemplo
        ({"V": 7, "A": 4, "R": 5, "K": 5}, "V").
        """
        conteo = {letra: 0 for letra in cls.ORDEN}
        for estilo in estilos_elegidos:
            if estilo not in conteo:
                raise ErrorValidacion(f"Estilo VARK desconocido: {estilo}")
            conteo[estilo] += 1

        maximo = max(conteo.values())
        if maximo == 0:
            raise ErrorValidacion("Debe seleccionar al menos una respuesta.")
        dominante = "".join(letra for letra in cls.ORDEN if conteo[letra] == maximo)
        return conteo, dominante

    @staticmethod
    def describir(dominante: str) -> str:
        if not dominante:
            return "Sin resultado"
        nombres = [ESTILOS_VARK[letra] for letra in dominante]
        if len(nombres) == 1:
            return nombres[0]
        return "Multimodal (" + ", ".join(nombres) + ")"

    @staticmethod
    def porcentajes(conteo: dict) -> dict:
        total = sum(conteo.values()) or 1
        return {k: round(v * 100 / total, 1) for k, v in conteo.items()}


class CalculadoraPersonalidad:
    """Calcula el tipo de personalidad (16 tipos)."""

    PARES = [DIMENSIONES[d][:2] for d in (1, 2, 3, 4)]

    @staticmethod
    def validar_par(puntos_a, puntos_b) -> None:
        """Reglas del PDF: enteros de 0 a 10, suman 10 y ninguno es 5."""
        try:
            a, b = int(puntos_a), int(puntos_b)
        except (TypeError, ValueError):
            raise ErrorValidacion("Los puntos deben ser números enteros.")
        if not (0 <= a <= 10 and 0 <= b <= 10):
            raise ErrorValidacion("Los puntos deben estar entre 0 y 10.")
        if a + b != 10:
            raise ErrorValidacion("Cada par debe sumar exactamente 10 puntos.")
        if a == 5 or b == 5:
            raise ErrorValidacion("No se permite usar el número 5.")

    @classmethod
    def calcular(cls, respuestas) -> tuple[dict, str]:
        """
        Recibe una lista de tuplas (letra_a, puntos_a, letra_b, puntos_b),
        por ejemplo [("E", 7, "I", 3), ...].
        Regresa (totales, tipo), por ejemplo
        ({"E": 32, "I": 58, ...}, "ISTJ").

        Empates: si las dos letras tienen los mismos puntos se elige la
        segunda (I, N, F o P), que es la convención del MBTI.
        """
        totales = {letra: 0 for par in cls.PARES for letra in par}
        for letra_a, puntos_a, letra_b, puntos_b in respuestas:
            cls.validar_par(puntos_a, puntos_b)
            totales[letra_a] += int(puntos_a)
            totales[letra_b] += int(puntos_b)

        tipo = "".join(a if totales[a] > totales[b] else b for a, b in cls.PARES)
        return totales, tipo

    @staticmethod
    def temperamento(tipo: str) -> dict:
        """ISTJ → letras 2 y 3 = 'ST' → Técnico analítico."""
        return TEMPERAMENTOS[tipo[1] + tipo[2]]
