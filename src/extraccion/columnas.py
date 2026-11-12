"""Estructura de columnas y subdivisiones de horarios de la ETSIIT.

Trabaja con páginas de pdfplumber y no interpreta asignaturas ni aulas.
"""

import re
from pathlib import Path
import sys

import pdfplumber

DIAS = ("lunes", "martes", "miércoles", "jueves", "viernes")
COLUMNAS = ("horas", *DIAS)
PATRON_HORA = re.compile(r"^\d{1,2}:\d{2}-\d{1,2}:\d{2}$")
PATRON_SUBGRUPO = re.compile(r"(?:\(?[A-F][1-3]\))", re.IGNORECASE)


def _agrupar_cabeceras(pagina):
    """Encuentra las cinco cabeceras de días de cada cuatrimestre."""
    palabras = pagina.extract_words()
    cabeceras = []
    for referencia in (p for p in palabras if p["text"].casefold() == "lunes"):
        centro_y = (referencia["top"] + referencia["bottom"]) / 2
        grupo = []
        for dia in DIAS:
            candidatos = [
                p for p in palabras
                if p["text"].casefold() == dia
                and abs((p["top"] + p["bottom"]) / 2 - centro_y) < 3
            ]
            if len(candidatos) != 1:
                break
            grupo.append(candidatos[0])
        if len(grupo) == len(DIAS):
            cabeceras.append(grupo)
    return sorted(cabeceras, key=lambda grupo: grupo[0]["top"])


def _limites_columnas(pagina, cabecera):
    """Encuentra los siete bordes verticales de las seis columnas principales."""
    y = sum((p["top"] + p["bottom"]) / 2 for p in cabecera) / len(cabecera)
    verticales = sorted({
        round(linea["x0"], 2)
        for linea in pagina.lines
        if abs(linea["x0"] - linea["x1"]) < 0.5
        and linea["top"] <= y + 4
        and linea["bottom"] >= y - 4
        and linea["bottom"] - linea["top"] >= 5
    })
    if not verticales:
        raise ValueError("No se encontraron líneas verticales en la cabecera")
    centros = [(p["x0"] + p["x1"]) / 2 for p in cabecera]
    objetivos = [
        centros[0] - (centros[1] - centros[0]) / 2,
        *((centros[i] + centros[i + 1]) / 2 for i in range(4)),
        centros[-1] + (centros[-1] - centros[-2]) / 2,
    ]
    limites_dias = [min(verticales, key=lambda x: abs(x - obj)) for obj in objetivos]
    anteriores = [x for x in verticales if x < limites_dias[0]]
    if not anteriores:
        raise ValueError("No se encontró el límite izquierdo de la columna de horas")
    limites = [min(anteriores), *limites_dias]
    if len(set(limites)) != 7 or limites != sorted(limites):
        raise ValueError("No se pudieron identificar las seis columnas principales")
    return limites


def extraer_columnas(pagina):
    """Devuelve las columnas principales de cada cuatrimestre de la página."""
    resultados = []
    for cabecera in _agrupar_cabeceras(pagina):
        limites = _limites_columnas(pagina, cabecera)
        resultados.append({
            "cabecera_y": round(sum(p["top"] for p in cabecera) / 5, 2),
            "columnas": [
                {"nombre": nombre, "x0": x0, "x1": x1}
                for nombre, x0, x1 in zip(COLUMNAS, limites[:-1], limites[1:])
            ],
        })
    return resultados


def _extraer_franjas_horarias(pagina, cabecera_y, limite_inferior, x0, x1):
    """Localiza las horas de una sola tabla, usando solo su columna horaria."""
    horas = sorted(
        (
            palabra for palabra in pagina.extract_words()
            if PATRON_HORA.fullmatch(palabra["text"])
            and cabecera_y < palabra["top"] < limite_inferior
            and x0 <= (palabra["x0"] + palabra["x1"]) / 2 < x1
        ),
        key=lambda p: p["top"],
    )
    franjas = []
    for indice, hora in enumerate(horas):
        if indice + 1 < len(horas):
            y1 = horas[indice + 1]["top"]
        else:
            paso = horas[-1]["top"] - horas[-2]["top"] if len(horas) >= 2 else 11
            y1 = min(hora["top"] + paso, limite_inferior)
        franjas.append({"etiqueta": hora["text"], "y0": hora["top"] - 3.0, "y1": y1 - 3.0})
    return franjas


def extraer_desdobles_en_celda(palabras, x0, x1, y0, y1):
    """Devuelve los espacios de las subcolumnas de una celda.

    Para esta versión del PDF, las subdivisiones usan etiquetas (A1), (A2),
    etc. No se cuentan palabras por separado: una clase puede tener varias.
    Las subcolumnas se distribuyen con anchura uniforme, según el issue #67.
    """
    contenido = [
        p for p in palabras
        if x0 <= (p["x0"] + p["x1"]) / 2 < x1
        and y0 <= (p["top"] + p["bottom"]) / 2 < y1
    ]
    if not contenido:
        return []

    marcadores = [p for p in contenido if PATRON_SUBGRUPO.search(p["text"])]
    cantidad = len(marcadores) if len(marcadores) >= 2 else 1
    if cantidad > 3:
        raise ValueError("Se han detectado más de tres subcolumnas en una celda")

    anchura = (x1 - x0) / cantidad
    return [
        {"x0": round(x0 + i * anchura, 2),
         "x1": round(x0 + (i + 1) * anchura, 2)}
        for i in range(cantidad)
    ]


def extraer_columnas_y_desdobles(pagina):
    """Devuelve columnas principales y subcolumnas por día y franja."""
    tablas = extraer_columnas(pagina)
    palabras = pagina.extract_words()
    resultados = []

    for indice, tabla in enumerate(tablas):
        cabecera_y = tabla["cabecera_y"]
        limite_inferior = (tablas[indice + 1]["cabecera_y"]
                           if indice + 1 < len(tablas) else pagina.height)
        columnas = tabla["columnas"]
        horas = columnas[0]
        franjas = _extraer_franjas_horarias(
            pagina, cabecera_y, limite_inferior, horas["x0"], horas["x1"]
        )
        filas = []
        for franja in franjas:
            dias = {}
            for columna in columnas[1:]:
                subcolumnas = extraer_desdobles_en_celda(
                    palabras, columna["x0"], columna["x1"],
                    franja["y0"], franja["y1"]
                )
                dias[columna["nombre"]] = {
                    "numero_desdobles": len(subcolumnas),
                    "subcolumnas": subcolumnas,
                }
            filas.append({"franja": franja["etiqueta"], "dias": dias})
        resultados.append({**tabla, "franjas": filas})
    return resultados
