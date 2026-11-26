from dataclasses import dataclass

from .asignatura import Asignatura
from .franja_horaria import FranjaHoraria


@dataclass(frozen=True)
class Clase:
    asignatura: Asignatura
    franja: FranjaHoraria
    aula: str
