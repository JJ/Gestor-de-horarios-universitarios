"""Extracción de columnas y subdivisiones de horarios de la ETSIIT.

Este módulo trabaja sobre páginas de ``pdfplumber`` y obtiene la estructura
geométrica de las tablas del horario. No interpreta asignaturas ni aulas.
"""

import re

DIAS = ("lunes", "martes", "miércoles", "jueves", "viernes")
COLUMNAS = ("horas", *DIAS)

PATRON_HORA = re.compile(r"^\d{1,2}:\d{2}-\d{1,2}:\d{2}$")
PATRON_SUBGRUPO = re.compile(r"(?:\(?[A-F][1-3]\))", re.IGNORECASE)


def _centro_vertical(palabra):
    """Devuelve la coordenada vertical central de una palabra."""
    return (palabra["top"] + palabra["bottom"]) / 2


def _centro_horizontal(palabra):
    """Devuelve la coordenada horizontal central de una palabra."""
    return (palabra["x0"] + palabra["x1"]) / 2


def _buscar_cabecera_dia(palabras, dia, centro_y):
    """Busca la cabecera de un día en una determinada fila."""
    candidatos = [
        palabra
        for palabra in palabras
        if palabra["text"].casefold() == dia
        and abs(_centro_vertical(palabra) - centro_y) < 3
    ]

    if len(candidatos) != 1:
        return None

    return candidatos[0]


def _crear_grupo_cabecera(palabras, referencia):
    """Construye una cabecera completa a partir de una referencia de lunes."""
    centro_y = _centro_vertical(referencia)

    grupo = [
        _buscar_cabecera_dia(palabras, dia, centro_y)
        for dia in DIAS
    ]

    if None in grupo:
        return None

    return grupo


def _agrupar_cabeceras(pagina):
    """Encuentra las cabeceras de días de cada cuatrimestre."""
    palabras = pagina.extract_words()

    referencias = [
        palabra
        for palabra in palabras
        if palabra["text"].casefold() == "lunes"
    ]

    grupos = [
        _crear_grupo_cabecera(palabras, referencia)
        for referencia in referencias
    ]

    cabeceras = [
        grupo
        for grupo in grupos
        if grupo is not None
    ]

    return sorted(cabeceras, key=lambda grupo: grupo[0]["top"])


def _extraer_lineas_verticales(pagina, y):
    """Obtiene las líneas verticales que atraviesan la cabecera."""
    verticales = {
        round(linea["x0"], 2)
        for linea in pagina.lines
        if abs(linea["x0"] - linea["x1"]) < 0.5
        and linea["top"] <= y + 4
        and linea["bottom"] >= y - 4
        and linea["bottom"] - linea["top"] >= 5
    }

    return sorted(verticales)


def _objetivos_limites_dias(cabecera):
    """Calcula las posiciones esperadas de los límites entre días."""
    centros = [
        _centro_horizontal(palabra)
        for palabra in cabecera
    ]

    limite_izquierdo = centros[0] - (centros[1] - centros[0]) / 2
    limite_derecho = centros[-1] + (centros[-1] - centros[-2]) / 2

    limites_interiores = [
        (centros[indice] + centros[indice + 1]) / 2
        for indice in range(len(centros) - 1)
    ]

    return [
        limite_izquierdo,
        *limites_interiores,
        limite_derecho,
    ]


def _buscar_limites_dias(verticales, objetivos):
    """Busca la línea vertical más cercana a cada límite esperado."""
    return [
        min(verticales, key=lambda x: abs(x - objetivo))
        for objetivo in objetivos
    ]


def _limites_columnas(pagina, cabecera):
    """Encuentra los siete límites de las seis columnas principales."""
    y = sum(
        _centro_vertical(palabra)
        for palabra in cabecera
    ) / len(cabecera)

    verticales = _extraer_lineas_verticales(pagina, y)

    if not verticales:
        raise ValueError(
            "No se encontraron líneas verticales en la cabecera"
        )

    objetivos = _objetivos_limites_dias(cabecera)
    limites_dias = _buscar_limites_dias(verticales, objetivos)

    anteriores = [
        x
        for x in verticales
        if x < limites_dias[0]
    ]

    if not anteriores:
        raise ValueError(
            "No se encontró el límite izquierdo de la columna de horas"
        )

    limites = [
        min(anteriores),
        *limites_dias,
    ]

    if len(set(limites)) != 7 or limites != sorted(limites):
        raise ValueError(
            "No se pudieron identificar las seis columnas principales"
        )

    return limites


def _crear_columnas(limites):
    """Construye las columnas principales a partir de sus límites."""
    return [
        {
            "nombre": nombre,
            "x0": x0,
            "x1": x1,
        }
        for nombre, x0, x1
        in zip(COLUMNAS, limites[:-1], limites[1:])
    ]


def _crear_tabla_columnas(pagina, cabecera):
    """Construye la estructura de columnas de una tabla."""
    limites = _limites_columnas(pagina, cabecera)

    return {
        "cabecera_y": round(
            sum(palabra["top"] for palabra in cabecera) / len(cabecera),
            2,
        ),
        "columnas": _crear_columnas(limites),
    }


def extraer_columnas(pagina):
    """Devuelve las columnas principales de cada cuatrimestre."""
    return [
        _crear_tabla_columnas(pagina, cabecera)
        for cabecera in _agrupar_cabeceras(pagina)
    ]


def _buscar_horas(pagina, cabecera_y, limite_inferior, x0, x1):
    """Localiza las franjas horarias dentro de una tabla."""
    horas = [
        palabra
        for palabra in pagina.extract_words()
        if PATRON_HORA.fullmatch(palabra["text"])
        and cabecera_y < palabra["top"] < limite_inferior
        and x0 <= _centro_horizontal(palabra) < x1
    ]

    return sorted(horas, key=lambda palabra: palabra["top"])


def _paso_ultima_franja(horas):
    """Calcula la separación vertical usada para la última franja."""
    if len(horas) >= 2:
        return horas[-1]["top"] - horas[-2]["top"]

    return 11


def _limite_ultima_franja(horas, indice, limite_tabla):
    """Estima el límite inferior de la última franja horaria."""
    paso = _paso_ultima_franja(horas)

    return min(
        horas[indice]["top"] + paso,
        limite_tabla,
    )


def _limite_inferior_franja(horas, indice, limite_tabla):
    """Calcula el límite inferior de una franja horaria."""
    if indice + 1 < len(horas):
        return horas[indice + 1]["top"]

    return _limite_ultima_franja(
        horas,
        indice,
        limite_tabla,
    )


def _crear_franjas(horas, limite_tabla):
    """Construye las franjas horarias de una tabla."""
    franjas = []

    for indice, hora in enumerate(horas):
        y1 = _limite_inferior_franja(
            horas,
            indice,
            limite_tabla,
        )

        franjas.append(
            {
                "etiqueta": hora["text"],
                "y0": hora["top"] - 3.0,
                "y1": y1 - 3.0,
            }
        )

    return franjas


def _extraer_franjas_horarias(
    pagina,
    cabecera_y,
    limite_inferior,
    x0,
    x1,
):
    """Extrae las franjas horarias de una tabla."""
    horas = _buscar_horas(
        pagina,
        cabecera_y,
        limite_inferior,
        x0,
        x1,
    )

    return _crear_franjas(horas, limite_inferior)


def _contenido_celda(palabras, x0, x1, y0, y1):
    """Obtiene las palabras contenidas dentro de una celda."""
    return [
        palabra
        for palabra in palabras
        if x0 <= _centro_horizontal(palabra) < x1
        and y0 <= _centro_vertical(palabra) < y1
    ]


def _cantidad_subcolumnas(contenido):
    """Calcula el número de subcolumnas de una celda."""
    marcadores = [
        palabra
        for palabra in contenido
        if PATRON_SUBGRUPO.search(palabra["text"])
    ]

    if len(marcadores) >= 2:
        return len(marcadores)

    return 1


def _crear_subcolumnas(x0, x1, cantidad):
    """Divide una celda en subcolumnas de igual anchura."""
    anchura = (x1 - x0) / cantidad

    return [
        {
            "x0": round(x0 + indice * anchura, 2),
            "x1": round(x0 + (indice + 1) * anchura, 2),
        }
        for indice in range(cantidad)
    ]


def extraer_desdobles_en_celda(palabras, x0, x1, y0, y1):
    """Devuelve las subcolumnas detectadas dentro de una celda."""
    contenido = _contenido_celda(
        palabras,
        x0,
        x1,
        y0,
        y1,
    )

    if not contenido:
        return []

    cantidad = _cantidad_subcolumnas(contenido)

    if cantidad > 3:
        raise ValueError(
            "Se han detectado más de tres subcolumnas en una celda"
        )

    return _crear_subcolumnas(
        x0,
        x1,
        cantidad,
    )


def _limite_inferior_tabla(pagina, tablas, indice):
    """Obtiene el límite inferior de una tabla."""
    if indice + 1 < len(tablas):
        return tablas[indice + 1]["cabecera_y"]

    return pagina.height


def _extraer_franjas_tabla(pagina, tabla, limite_inferior):
    """Obtiene las franjas horarias de una tabla."""
    columna_horas = tabla["columnas"][0]

    return _extraer_franjas_horarias(
        pagina,
        tabla["cabecera_y"],
        limite_inferior,
        columna_horas["x0"],
        columna_horas["x1"],
    )


def _extraer_desdobles_dia(palabras, columna, franja):
    """Obtiene los desdobles de un día en una franja concreta."""
    subcolumnas = extraer_desdobles_en_celda(
        palabras,
        columna["x0"],
        columna["x1"],
        franja["y0"],
        franja["y1"],
    )

    return {
        "numero_desdobles": len(subcolumnas),
        "subcolumnas": subcolumnas,
    }


def _extraer_dias(palabras, columnas, franja):
    """Obtiene los desdobles de todos los días de una franja."""
    return {
        columna["nombre"]: _extraer_desdobles_dia(
            palabras,
            columna,
            franja,
        )
        for columna in columnas[1:]
    }


def _crear_filas(palabras, columnas, franjas):
    """Construye las filas de una tabla."""
    return [
        {
            "franja": franja["etiqueta"],
            "dias": _extraer_dias(
                palabras,
                columnas,
                franja,
            ),
        }
        for franja in franjas
    ]


def _procesar_tabla(pagina, palabras, tablas, indice):
    """Procesa las franjas y desdobles de una tabla."""
    tabla = tablas[indice]

    limite_inferior = _limite_inferior_tabla(
        pagina,
        tablas,
        indice,
    )

    franjas = _extraer_franjas_tabla(
        pagina,
        tabla,
        limite_inferior,
    )

    filas = _crear_filas(
        palabras,
        tabla["columnas"],
        franjas,
    )

    return {
        **tabla,
        "franjas": filas,
    }


def extraer_columnas_y_desdobles(pagina):
    """Devuelve columnas y desdobles de cada tabla de la página."""
    tablas = extraer_columnas(pagina)
    palabras = pagina.extract_words()

    return [
        _procesar_tabla(
            pagina,
            palabras,
            tablas,
            indice,
        )
        for indice in range(len(tablas))
    ]
