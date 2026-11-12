import re


def extract_course_year(url: str) -> str:
    """Extrae el año académico `n-n` de una URL PDF.

    Args:
        url: URL del PDF del horario.

    Returns:
        El año académico encontrado, por ejemplo, ``"26-27"``.

    Raises:
        ValueError: Si la URL no contiene un año académico válido.
    """
    match = re.search(
        r"(?:\(|%28)(\d{2}-\d{2})(?:\)|%29)(?=\.pdf(?:$|[?#]))", url, re.IGNORECASE
    )
    if not match:
        raise ValueError("La URL no contiene un año académico válido.")
    return match.group(1)
