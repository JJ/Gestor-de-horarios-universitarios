from dataclasses import dataclass


@dataclass(frozen=True)
class Asignatura:
    siglas: str
    nombre: str
    grupo: str
    subgrupo: str | None
    cuatrimestre: int
