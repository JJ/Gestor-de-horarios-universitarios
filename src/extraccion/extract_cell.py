import re
from typing import List, Dict, Optional
import pdfplumber


def extract_schedule_cell(
    pdf_path: str,
    table_name: str,
    semester: str,
    time_slot: str,
    weekday: str
) -> List[Dict[str, str]]:
    """Extrae el contenido de una celda del horario universitario.

    Args:
        pdf_path: Ruta al archivo PDF del horario.
        table_name: Nombre del curso (ej: "1º A Grado en Ingeniería Informática").
        semester: Cuatrimestre ("1er. cuatrimestre" o "2º cuatrimestre").
        time_slot: Franja horaria (ej: "9:30-10:30" o "10:30-11:30").
        weekday: Día de la semana (Lunes, Martes, Miércoles, Jueves, Viernes).

    Returns:
        Lista de diccionarios con el contenido de la celda. Cada elemento contiene:
        - 'asignatura': Nombre de asignatura con subgrupo (ej: "IG (B1)", "FS")
        - 'aula': Aula/laboratorio (ej: "lab. 0.2", "3.7", "0.6")
        Lista vacía si la celda está vacía.

    Raises:
        ValueError: Si no se encuentra la tabla, cuatrimestre o celda especificada.
        FileNotFoundError: Si el PDF no existe.
    """
    weekday = weekday.strip().capitalize()
    time_slot = _normalize_time_slot(time_slot)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Buscar en todas las páginas
            for page in pdf.pages:
                tables = page.extract_tables()
                
                for table in tables:
                    if not table or len(table) < 2:
                        continue
                    
                    if _is_target_table(table, table_name, semester):
                        result = _extract_cell_from_table(table, time_slot, weekday)
                        if result is not None:
                            return result
            
            raise ValueError(
                f"No se encontró la tabla '{table_name}' con cuatrimestre '{semester}'"
            )
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {pdf_path}")


def _normalize_time_slot(time_slot: str) -> str:
    """Normaliza la franja horaria al formato estándar."""
    time_slot = time_slot.strip()
    parts = time_slot.split('-')
    
    normalized_parts = []
    for part in parts:
        part = part.strip()
        if ':' in part:
            hour, minute = part.split(':')
            if len(hour) == 1:
                hour = '0' + hour
            normalized_parts.append(f"{hour}:{minute}")
        else:
            normalized_parts.append(part)
    
    return '-'.join(normalized_parts)


def _is_target_table(table: List[List[str]], table_name: str, semester: str) -> bool:
    """Verifica si una tabla es la buscada."""
    header_text = ""
    for i in range(min(3, len(table))):
        row_text = " ".join([cell or "" for cell in table[i]])
        header_text += row_text + " "
    
    # Verificar que contiene el nombre de la tabla y el cuatrimestre
    return table_name in header_text and semester in header_text


def _extract_cell_from_table(
    table: List[List[str]], 
    time_slot: str, 
    weekday: str
) -> Optional[List[Dict[str, str]]]:
    """Extrae el contenido de una celda específica de la tabla."""
    header_row_idx = None
    for idx, row in enumerate(table):
        if any(weekday in (cell or "") for cell in row):
            header_row_idx = idx
            break
    
    if header_row_idx is None:
        raise ValueError(f"No se encontró el día '{weekday}' en la tabla")
    
    day_columns = []
    for col_idx, cell in enumerate(table[header_row_idx]):
        if cell and weekday in cell:
            # Esta columna y las siguientes None pertenecen a este día
            day_columns.append(col_idx)
            # Buscar columnas None adicionales que pertenezcan al mismo día
            for next_col in range(col_idx + 1, len(table[header_row_idx])):
                next_cell = table[header_row_idx][next_col]
                # Si es None o vacío, pertenece al día actual
                if not next_cell or next_cell.strip() == '':
                    day_columns.append(next_col)
                else:
                    break
            break
    
    if not day_columns:
        raise ValueError(f"No se encontraron columnas para el día '{weekday}'")
    
    time_row_idx = None
    for idx in range(header_row_idx + 1, len(table)):
        first_cell = (table[idx][0] or "").strip()
        # Normalizar ambos formatos para comparar
        normalized_first = _normalize_time_slot(first_cell) if ':' in first_cell else first_cell
        if time_slot in first_cell or time_slot == normalized_first:
            time_row_idx = idx
            break
        time_slot_alt = time_slot.replace('0', '', 1) if time_slot.startswith('0') else '0' + time_slot.split('-')[0] + '-' + time_slot.split('-')[1]
        if time_slot_alt in first_cell:
            time_row_idx = idx
            break
    
    if time_row_idx is None:
        raise ValueError(f"No se encontró la franja horaria: {time_slot}")
    
    result = []
    for col_idx in day_columns:
        if col_idx < len(table[time_row_idx]):
            cell_content = table[time_row_idx][col_idx]
            if cell_content and cell_content.strip():
                # Parsear el contenido de la celda
                parsed = _parse_cell_content(cell_content)
                result.extend(parsed)
    
    return result


def _parse_cell_content(cell_content: str) -> List[Dict[str, str]]:
    """Parsea el contenido de una celda para extraer asignaturas y aulas.
    
    El formato puede ser:
    - Una línea: "ASIGNATURA\nAULA" 
    - O separado por espacios: "ASIG1 (G1) ASIG2 (G2)\nAULA1 AULA2"
    """
    if not cell_content or not cell_content.strip():
        return []
    
    lines = cell_content.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    
    if not lines:
        return []
    
    result = []
    
    if len(lines) == 1:
        # Puede haber múltiples asignaturas separadas por espacios
        asignaturas = _split_subjects(lines[0])
        for asig in asignaturas:
            result.append({'asignatura': asig, 'aula': ''})
        return result
    
    asignaturas_line = lines[0]
    aulas_lines = lines[1:]
    
    asignaturas = _split_subjects(asignaturas_line)
    
    aulas_line = ' '.join(aulas_lines)
    
    aulas = _split_classrooms(aulas_line)
    
    for i, asig in enumerate(asignaturas):
        aula = aulas[i] if i < len(aulas) else ''
        result.append({'asignatura': asig, 'aula': aula})
    
    return result


def _split_subjects(text: str) -> List[str]:
    """Separa múltiples asignaturas de una línea.
    
    Ejemplos:
    - "FP (B1)" -> ["FP (B1)"]
    - "FP (B1) FFT (B2) ALEM (B3)" -> ["FP (B1)", "FFT (B2)", "ALEM (B3)"]
    - "FS" -> ["FS"]
    """
    pattern = r'[A-Z]+(?:\s*\([A-Z]\d+\))?'
    matches = re.findall(pattern, text)
    
    return [m.strip() for m in matches if m.strip()]


def _split_classrooms(text: str) -> List[str]:
    """Separa múltiples aulas de una línea.
    
    Ejemplos:
    - "2.1" -> ["2.1"]
    - "2.1 3.6 1.7" -> ["2.1", "3.6", "1.7"]
    - "lab. 0.2" -> ["lab. 0.2"]
    - "0.6 (ed. auxiliar)" -> ["0.6 (ed. auxiliar)"]
    - "1.5/2.3" -> ["1.5/2.3"]
    """
    text = text.strip()
    
    if not text:
        return []
    
    aulas = []
    pattern = r'(?:lab\.\s*)?\d+(?:\.\d+)?(?:/\d+(?:\.\d+)?)?(?:\s*\([^)]+\))?'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    return [m.strip() for m in matches if m.strip()]
