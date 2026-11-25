"""
Generación del PDF con la ficha técnica del resultado (individual, grupal o total).
Responsable: Lui

Usa la librería ReportLab.
"""
from datetime import datetime
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.data.instrumentos import DESCRIPCION_VARK, ESTRATEGIAS_VARK
from app.services.calculos import (
    DIMENSIONES,
    ESTILOS_VARK,
    NOMBRES_LETRAS,
    CalculadoraPersonalidad,
    CalculadoraVark,
)
from app.services.estadisticas_service import Estadisticas

ROJO = colors.HexColor("#a3120a")
GRIS = colors.HexColor("#2b2b2b")
GRIS_CLARO = colors.HexColor("#eeeeee")


class ReportePDF:
    def __init__(self):
        estilos = getSampleStyleSheet()
        self.titulo = ParagraphStyle("titulo", parent=estilos["Title"], textColor=ROJO, fontSize=18)
        self.subtitulo = ParagraphStyle("sub", parent=estilos["Heading2"], textColor=GRIS, spaceBefore=10)
        self.h3 = ParagraphStyle("h3", parent=estilos["Heading3"], textColor=ROJO)
        self.normal = estilos["BodyText"]
        self.pie = ParagraphStyle("pie", parent=estilos["BodyText"], fontSize=8,
                                  textColor=colors.grey, alignment=TA_CENTER)

    # ------------------------------------------------------------ utilidades
    def _tabla(self, datos, anchos=None):
        tabla = Table(datos, colWidths=anchos, hAlign="LEFT")
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), GRIS),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, GRIS_CLARO]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        return tabla

    def _grafica_barras(self, etiquetas, valores, ancho=15 * cm, alto=5.5 * cm):
        dibujo = Drawing(ancho, alto)
        grafica = VerticalBarChart()
        grafica.x, grafica.y = 30, 25
        grafica.width, grafica.height = ancho - 50, alto - 40
        grafica.data = [list(valores) or [0]]
        grafica.categoryAxis.categoryNames = list(etiquetas)
        grafica.categoryAxis.labels.fontSize = 8
        grafica.valueAxis.valueMin = 0
        grafica.valueAxis.labels.fontSize = 8
        grafica.bars[0].fillColor = ROJO
        dibujo.add(grafica)
        return dibujo

    def _lista(self, elementos):
        return ListFlowable(
            [ListItem(Paragraph(e, self.normal), leftIndent=12) for e in elementos],
            bulletType="bullet", start="•",
        )

    def _encabezado(self, titulo, subtitulo):
        return [
            Paragraph("Aprendizaje VARK y Test de Personalidad", self.titulo),
            Paragraph(f"Ficha técnica — {titulo}", self.subtitulo),
            Paragraph(subtitulo, self.normal),
            Paragraph(f"Fecha de emisión: {datetime.now():%d/%m/%Y %H:%M}", self.normal),
            Spacer(1, 0.4 * cm),
        ]

    def _construir(self, elementos) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=2 * cm, rightMargin=2 * cm,
                                topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                                title="Ficha técnica VARK y Personalidad")
        elementos.append(Spacer(1, 0.6 * cm))
        elementos.append(Paragraph(
            "Instrumentos: VARK (Neil Fleming, 2006) y Test basado en la tipología de Jung y Myers-Briggs.",
            self.pie))
        doc.build(elementos)
        return buffer.getvalue()

    # ------------------------------------------------------------ individual
    def individual(self, alumno) -> bytes:
        e = self._encabezado(
            escape(alumno.nombre),
            f"Matrícula: <b>{escape(alumno.matricula)}</b> &nbsp; Carrera: <b>{escape(alumno.carrera)}</b> &nbsp; "
            f"Semestre: <b>{alumno.semestre}</b> &nbsp; Grupo: <b>{escape(alumno.grupo)}</b>",
        )

        vark = alumno.ultimo_vark
        e.append(Paragraph("1. Estilo de aprendizaje VARK", self.subtitulo))
        if vark:
            conteo = vark.conteo
            pct = CalculadoraVark.porcentajes(conteo)
            filas = [["Estilo", "Puntos", "%"]] + [
                [ESTILOS_VARK[k], conteo[k], f"{pct[k]}%"] for k in "VARK"
            ]
            e.append(self._tabla(filas, [6 * cm, 3 * cm, 3 * cm]))
            e.append(Spacer(1, 0.3 * cm))
            e.append(self._grafica_barras([ESTILOS_VARK[k] for k in "VARK"], [conteo[k] for k in "VARK"]))
            e.append(Paragraph(f"Estilo dominante: <b>{vark.descripcion}</b> "
                               f"(aplicado el {vark.fecha:%d/%m/%Y})", self.normal))
            for letra in vark.estilo_dominante:
                e.append(Paragraph(f"Estrategias sugeridas — {ESTILOS_VARK[letra]}", self.h3))
                e.append(Paragraph(DESCRIPCION_VARK[letra], self.normal))
                e.append(self._lista(ESTRATEGIAS_VARK[letra]))
        else:
            e.append(Paragraph("El alumno todavía no contesta el cuestionario VARK.", self.normal))

        pers = alumno.ultima_personalidad
        e.append(Paragraph("2. Tipo de personalidad (Jung / Myers-Briggs)", self.subtitulo))
        if pers:
            t = pers.totales
            filas = [["Dimensión", "Preferencia", "Puntos", "Preferencia", "Puntos"]]
            for d in (1, 2, 3, 4):
                a, b, nombre = DIMENSIONES[d]
                filas.append([Paragraph(nombre, self.normal), NOMBRES_LETRAS[a], t[a], NOMBRES_LETRAS[b], t[b]])
            e.append(self._tabla(filas, [6 * cm, 3.2 * cm, 1.6 * cm, 3.2 * cm, 1.6 * cm]))
            temp = CalculadoraPersonalidad.temperamento(pers.tipo_codigo)
            e.append(Spacer(1, 0.3 * cm))
            e.append(Paragraph(f"Tipo: <b>{pers.tipo_codigo}</b> &nbsp; — &nbsp; Temperamento: "
                               f"<b>{temp['nombre']}</b> (motivador: {temp['motivador'].lower()}; "
                               f"evitarle: {temp['evitar'].lower()})", self.normal))
            e.append(Paragraph("Peligros potenciales", self.h3))
            e.append(self._lista(pers.tipo.lista_peligros))
            e.append(Paragraph("Sugerencias para el desarrollo", self.h3))
            e.append(self._lista(pers.tipo.lista_sugerencias))
        else:
            e.append(Paragraph("El alumno todavía no contesta el test de personalidad.", self.normal))

        return self._construir(e)

    # ------------------------------------------------------- grupal / total
    def grupal(self, alumnos, titulo: str) -> bytes:
        est = Estadisticas(alumnos)
        r = est.resumen()
        e = self._encabezado(
            escape(titulo),
            f"Alumnos: <b>{r['total_alumnos']}</b> &nbsp; Con VARK: <b>{r['con_vark']}</b> &nbsp; "
            f"Con test de personalidad: <b>{r['con_personalidad']}</b>",
        )

        e.append(Paragraph("1. Estilos de aprendizaje VARK", self.subtitulo))
        suma, prom = r["vark"]["suma"], r["vark"]["promedio"]
        filas = [["Estilo", "Puntos totales", "Promedio por alumno"]] + [
            [ESTILOS_VARK[k], suma[k], prom[k]] for k in "VARK"
        ]
        e.append(self._tabla(filas, [6 * cm, 4 * cm, 4 * cm]))
        e.append(self._grafica_barras([ESTILOS_VARK[k] for k in "VARK"], [suma[k] for k in "VARK"]))
        e.append(Paragraph(f"Estilo predominante del grupo: <b>{r['vark']['dominante_global']}</b>", self.normal))
        dom = r["vark"]["dominantes"]
        e.append(Paragraph("Alumnos por estilo dominante", self.h3))
        e.append(self._tabla([["Estilo", "Alumnos"]] + [[k, v] for k, v in dom.items()], [6 * cm, 3 * cm]))

        e.append(Paragraph("2. Tipos de personalidad", self.subtitulo))
        tipos = r["personalidad"]["tipos"]
        if tipos:
            e.append(self._grafica_barras(list(tipos.keys()), list(tipos.values())))
            e.append(Paragraph(f"Tipo más común: <b>{r['personalidad']['tipo_mas_comun']}</b>", self.normal))
            e.append(Paragraph("Temperamentos", self.h3))
            temp = r["personalidad"]["temperamentos"]
            e.append(self._tabla([["Temperamento", "Alumnos"]] + [[k, v] for k, v in temp.items()],
                                 [6 * cm, 3 * cm]))
            e.append(Paragraph("Preferencias", self.h3))
            letras = r["personalidad"]["letras"]
            filas = [["Dimensión", "Preferencia", "Alumnos", "Preferencia", "Alumnos"]]
            for d in (1, 2, 3, 4):
                a, b, nombre = DIMENSIONES[d]
                filas.append([Paragraph(nombre, self.normal), NOMBRES_LETRAS[a], letras[a], NOMBRES_LETRAS[b], letras[b]])
            e.append(self._tabla(filas, [6 * cm, 3.2 * cm, 1.6 * cm, 3.2 * cm, 1.6 * cm]))
        else:
            e.append(Paragraph("Ningún alumno de este grupo ha contestado el test de personalidad.", self.normal))

        e.append(Paragraph("3. Detalle por alumno", self.subtitulo))
        filas = [["Matrícula", "Nombre", "Grupo", "VARK", "Tipo"]]
        for a in est.alumnos:
            filas.append([
                a.matricula,
                Paragraph(escape(a.nombre), self.normal),
                f"{a.semestre}° {a.grupo}",
                a.ultimo_vark.estilo_dominante if a.ultimo_vark else "—",
                a.ultima_personalidad.tipo_codigo if a.ultima_personalidad else "—",
            ])
        e.append(self._tabla(filas, [2.8 * cm, 7 * cm, 2.2 * cm, 2 * cm, 2 * cm]))
        return self._construir(e)
